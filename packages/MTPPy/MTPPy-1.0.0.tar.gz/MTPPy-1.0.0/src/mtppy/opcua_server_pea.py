from opcua import Server, ua
from mtppy.communication_object import OPCUACommunicationObject
from mtppy.service import Service
from mtppy.suc_data_assembly import SUCActiveElement


class OPCUAServerPEA:
    def __init__(self, mtp_generator, endpoint='opc.tcp://0.0.0.0:4840/'):
        self.service_set = {}
        self.active_elements = {}
        self.endpoint = endpoint
        self.opcua_server = None
        self.opcua_ns = 3
        self.subscription_list = SubscriptionList()
        self.init_opcua_server()
        self.mtp = mtp_generator

    def add_service(self, service: Service):
        self.service_set[service.tag_name] = service

    def add_active_element(self, active_element: SUCActiveElement):
        self.active_elements[active_element.tag_name] = active_element

    def init_opcua_server(self):
        self.opcua_server = Server()
        self.opcua_server.set_endpoint(self.endpoint)
        # self.opcua_ns = self.opcua_server.register_namespace('namespace_idx')

    def get_opcua_server(self):
        return self.opcua_server

    def get_opcua_ns(self):
        return self.opcua_ns

    def run_opcua_server(self):
        self.opcua_server.start()
        self.build_opcua_server()
        self.start_subscription()
        # self.set_services_in_idle()

    def set_services_in_idle(self):
        for service in self.service_set.values():
            service.init_idle_state()

    def build_opcua_server(self):
        ns = self.opcua_ns
        server = self.opcua_server.get_objects_node()

        services_node_id = f'ns={ns};s=services'
        services_node = server.add_folder(services_node_id, "services")

        # initiate a new MTP that will be added to InstanceHierarchy: ModuleTypePackage
        self.mtp.add_module_type_package('1.0.0', name='mtp_test', description='')

        # add InternalElement opcua server to ModuleTypePackage/CommunicationSet/SourceList
        self.mtp.add_opcua_server(self.endpoint)

        for service in self.service_set.values():
            self._create_opcua_objects_for_folders(service, services_node_id, services_node)

        act_elem_node_id = f'ns={ns};s=active_elements'
        act_elem_node = server.add_folder(act_elem_node_id, "active_elements")
        for active_element in self.active_elements.values():
            self._create_opcua_objects_for_folders(active_element, act_elem_node_id, act_elem_node)

        # add SupportedRoleClass to all InternalElements
        self.mtp.apply_add_supported_role_class()

        # export manifest.aml
        self.mtp.export_manifest()

    def _create_opcua_objects_for_folders(self, data_assembly, parent_opcua_prefix, parent_opcua_object):
        da_node_id = f'{parent_opcua_prefix}.{data_assembly.tag_name}'
        da_node = parent_opcua_object.add_folder(da_node_id, data_assembly.tag_name)

        # type of data assembly (e.g. services, active_elements, procedures etc.)
        da_type = parent_opcua_prefix.split('=')[-1].split('.')[-1]

        folders = ['configuration_parameters',
                   'procedures',
                   'procedure_parameters', 'process_value_ins', 'report_values', 'process_value_outs']
        leaves = ['op_src_mode', 'state_machine', 'procedure_control']

        # create instance of  ServiceControl, HealthStateView, DIntServParam etc.
        instance = self.mtp.create_instance(data_assembly, da_node_id)

        link_id = self.mtp.random_id_generator()
        if da_type == 'services' or da_type in folders:
            link_id = self.mtp.create_components_for_services(data_assembly, da_type)

        if hasattr(data_assembly, 'attributes'):
            self._create_opcua_objects_for_leaves(data_assembly, da_node_id, da_node, instance)

        for section_name in folders + leaves:
            if not hasattr(data_assembly, section_name):
                continue
            section = eval(f'data_assembly.{section_name}')
            section_node_id = f'{da_node_id}.{section_name}'
            print(section_node_id)
            section_node = da_node.add_folder(section_node_id, section_name)
            if section_name in folders:
                for parameter in eval(f'data_assembly.{section_name}.values()'):
                    self._create_opcua_objects_for_folders(parameter, section_node_id, section_node)
            if section_name in leaves:
                self._create_opcua_objects_for_leaves(section, section_node_id, section_node, instance)

        # create linked obj between instance and service component
        self.mtp.add_linked_attr(instance, link_id)

    def _create_opcua_objects_for_leaves(self, object, parent_opcua_prefix, parent_opcua_object, par_instance):
        """
        :param par_instance: instance under InstanceHierarchy_MTP/CommunicationSet/InstanceList
        :param par_component: element under InstanceHierarchy_Service or InstanceHierarchy_Service (HMI is not implemented)
        """
        for attr in object.attributes.values():
            attribute_node_id = f'{parent_opcua_prefix}.{attr.name}'

            # We attach communication objects to be able to write values on opcua server on attributes change
            opcua_type = self.infere_data_type(attr.type)
            opcua_node_obj = parent_opcua_object.add_variable(attribute_node_id, attr.name, attr.init_value,
                                                              varianttype=opcua_type)
            print(f'OPCUA Node: {attribute_node_id}, Name: {attr.name}, Value: {attr.init_value}')
            opcua_node_obj.set_writable(False)
            opcua_comm_obj = OPCUACommunicationObject(opcua_node_obj, node_id=opcua_node_obj)
            attr.attach_communication_object(opcua_comm_obj)

            linked_id = self.mtp.random_id_generator()  # create linked-id for opc ua node
            # add opc ua node and its attributes to ModuleTypePackage/CommunicationSet/SourceList/OPCUAServer
            self.mtp.add_external_interface(attribute_node_id, self.opcua_ns, linked_id)

            """
            add attributes of data assembly to corresponding instance under InstanceList 
            e.g.: attributes of services belong to InstanceList/ServiceControl

            exception: some attributes of procedure ('ProcedureId', 'IsSelfCompleting', 'IsDefault') should be 
            added to InstanceHierarchy_Service/service/procedure. The other attributes of procedure should belong to 
            InstanceList/HeathStateView
            """
            if type(object).__name__ == 'Procedure' and attr.name in ['ProcedureId', 'IsSelfCompleting', 'IsDefault']:
                pass
            else:
                self.mtp.add_attr_to_instance(par_instance, attr.name, attr.init_value, linked_id)

            # We subscribe to nodes that are writable attributes
            if attr.sub_cb is not None:
                opcua_node_obj.set_writable(True)
                self.subscription_list.append(opcua_node_obj, attr.sub_cb)

    def infere_data_type(self, attribute_data_type):
        if attribute_data_type == int:
            return ua.VariantType.Int64
        elif attribute_data_type == float:
            return ua.VariantType.Float
        elif attribute_data_type == bool:
            return ua.VariantType.Boolean
        elif attribute_data_type == str:
            return ua.VariantType.String
        else:
            return None

    def start_subscription(self):
        handler = Marshalling()
        handler.import_subscription_list(self.subscription_list)
        sub = self.opcua_server.create_subscription(500, handler)
        handle = sub.subscribe_data_change(self.subscription_list.get_nodeid_list())


class SubscriptionList:
    def __init__(self):
        self.sub_list = {}

    def append(self, node_id, cb_value_change):
        identifier = node_id.nodeid.Identifier
        self.sub_list[identifier] = {'node_id': node_id, 'callback': cb_value_change}

    def get_nodeid_list(self):
        if len(self.sub_list) == 0:
            return None
        else:
            node_id_list = []
            for node_id in self.sub_list.values():
                node_id_list.append(node_id['node_id'])
            return node_id_list

    def get_callback(self, node_id):
        identifier = node_id.nodeid.Identifier
        if identifier in self.sub_list.keys():
            return self.sub_list[identifier]['callback']
        else:
            return None


class Marshalling(object):
    def __init__(self):
        self.subscription_list = None

    def import_subscription_list(self, subscription_list: SubscriptionList):
        self.subscription_list = subscription_list

    def datachange_notification(self, node, val, data):
        # print("Data change event", node, val)
        callback = self.find_set_callback(node)
        if callback is not None:
            try:
                callback(val)
            except Exception as exc:
                print(f'Something wrong with callback {callback}: {exc}')

    def find_set_callback(self, node_id):
        return self.subscription_list.get_callback(node_id)
