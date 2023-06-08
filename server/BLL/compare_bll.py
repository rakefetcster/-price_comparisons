from DAL.compare_file_dal import CompareFileDal
import BLL.webscrape as wb


class CompareBL:
    def __init__(self):
        self.__compare_file_dal=CompareFileDal()

    def get_data(self,link_to_file):
        obj_list = list()
        data = self.__compare_file_dal.read_file(link_to_file)
        if "Error" in data:
            return data
        for i,word in enumerate(data):
            if i==0:
                the_list = list()
                for j in range(len(data.index)):
                   the_list.append(data.iloc[j, 0])
                obj_list.append(the_list)
            if i==2:
                the_list = list()
                for j in range(len(data.index)):
                    the_list.append((data.iloc[j, 2]))
                obj_list.append(the_list)
        links , item_stores_prices , indexes, indexes_prices = wb.web_scrape_all_information(obj_list[0],obj_list[1])
        data_fix,only_red_dict = self.fix_table_data(data,links , item_stores_prices , indexes, indexes_prices)
        data = self.__compare_file_dal.write_file(link_to_file,data,data_fix)
        return only_red_dict

    def fix_table_data(self,data,links , item_stores_prices , indexes, indexes_prices):
        final_list = list()
        only_red_dict = dict()
        list_of_list_red = list()
            
        for i,row in enumerate(data.index):
            row_list = list()
            only_red_list1 = list()
            
            for val in data.columns:
                only_red_list1.append(val)
            only_red_list1.reverse()
            only_red_dict["header"] = only_red_list1
            if str(data.iloc[i, 14]) != str(data.iloc[i, 15]):
                for j in range(0,16):
                    row_list.append(str(data.iloc[i, j]))
                row_list.reverse()
                list_of_list_red.append(row_list)
                
            only_red_dict["body"] = list_of_list_red
            this_list = list()
            this_list = [data.iloc[i, 0],links[i],data.iloc[i, 2],indexes_prices[i],item_stores_prices[i][0][1],item_stores_prices[i][0][0],item_stores_prices[i][1][1],item_stores_prices[i][1][0],item_stores_prices[i][2][1],item_stores_prices[i][2][0],item_stores_prices[i][3][1],item_stores_prices[i][3][0],item_stores_prices[i][4][1],item_stores_prices[i][4][0],indexes[i],data.iloc[i, 14]]
            final_list.append(this_list)
        return final_list,only_red_dict
            

    def get_user_name(self,id):
        userObj = self.__factory_db_dal.user_exist("_id",id)
        return {"user_name":userObj['FullName'] }

    