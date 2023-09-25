from src.handlers.handle_server import server_list

class all_servers():
    def create_connection(self):
        for server in server_list:
            server_list[server].create_connection()

    def close_connection(self):
        for server in server_list:
            server_list[server].close_connection

    def upload_plugin(self, file):
        for server in server_list:
            server_list[server].upload_plugin(file)

    def upload_server_jar(self, file):
        pass

    def list_plugins(self):
        combined = []
        for server in server_list:
            combined += server_list[server].list_plugins()
        return combined
    
    def list_server_root(self):
        pass
    
    def download_plugin(self, file, dest):
        for server in server_list:
            server_list[server].download_plugin(self, file, dest)

    def validate_plugin(self, plugin_file):
        pass
        
    def delete_plugin(self, file):
        for server in server_list:
            server_list[server].delete_plugin(self, file)

    def delete_server_jar(self, file):
        pass