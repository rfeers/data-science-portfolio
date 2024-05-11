import pandas as pd
import numpy as np
import os

# Static info
## We define the regions lists to be used for each country

## France, Germany, Italy, UK, Belgium, Netherlands and Sweden contain: 
European_regions = ["Catalonia","Andalusia","Basque Country","Balearic Islands","Asturias","Navarre","Valencia",
                    "Canary Islands","Galicia","Madrid","Sardinia","Algarve","Tuscany","Croatia","Sicily",
                    "Provence-French Alps-French Riviere","Andorra","Corsica","Greek islands","Swiss Alps",
                    "Brittany / La Bretagne","Scotland","French Pyrenees","Austrian Alps","None of these"]

## Spain contains: 
Spanish_regions = ['Catalonia','Andalusia','Basque Country','Balearic Islands','Asturias','Navarre','Valencia',
                'Canary Islands','Galicia','Madrid','Sardinia','Algarve','Tuscany','Croatia','Sicily',
                'Provence-French Alps-French Riviere','Andorra','Extremadura','Castilla la Mancha',
                'Castilla y León','Cantabria','La Rioja','Murcia','Aragón',"None of these"]

## USA contains: 
American_regions = ["Catalonia","Madrid","San Sebastian","Costa del Sol","Andalusia","Basque Country",
                    "Barcelona","Balearic Islands","Ibiza","Portugal","Italy","Paris","Greek Islands",
                    "Croatia","London","Scotland","Ireland","Iceland","Switzerland","Germany","Tuscany",
                    "French Riviera","None of these"]

#Dictionary with countries and regions to be used
Regions_dict = {'ES': Spanish_regions,
                'DE': European_regions,
                'SE':  European_regions,
                'FR':  European_regions,
                'NL':  European_regions,
                'BE':  European_regions,
                'IT':  European_regions,
                "UK":  European_regions,
                "US":  American_regions
            }

## We define the wanted structure of our output tables
answer_region_heads = [
                        "case_id", 

                        "aided","buzz","imp","qual","value","rep","sat","rec",

                        "Q5_1","Q5_2","Q5_3","Q5_4","Q5_5",
                        "Q5_6","Q5_7","Q5_8","Q5_9","Q5_10",
                        "Q5_11","Q5_12","Q5_13","Q5_14","Q5_15",
                        "Q5_16","Q5_17","Q5_18","Q5_19","Q5_20",

                        "Q4_1","Q4_2","Q4_3","Q4_4","Q4_5",
                        "Q4_6","Q4_7","Q4_8","Q4_9","Q4_10",
                        "Q4_11","Q4_12","Q4_13","Q4_14","Q4_15",
                        "Q4_16","Q4_17","Q4_18","Q4_19","Q4_20",
    
                        "adaware_db","wom_db","ever_own_db","current_own_db","consider_db",
                        
                        "Dest", "Country"
] 


answer_region_heads_none_these = [
                        "case_id", 
                        "adaware_db","wom_db","ever_own_db","current_own_db","consider_db",
                        "Dest", "Country"
] 

# Loading support file - STRUCTURE
structure = pd.read_csv("Support/Estructura_RLD.csv", delimiter=";")

structure_main     = structure[structure["BBDD"]=="Main"]
structure_generica = structure[structure["BBDD"]=="Generica_enquestat"]
structure_regions  = structure[structure["BBDD"]=="Respostes_regions"]

def get_data(pathname: str, Q: str) -> dict:
    # Initialize void variables
    country_dict = {}
    country_list = []

    # For each file, we get both the file name and the table
    for filename in os.listdir(pathname):
        try:
            country_name = filename.split("DestinationIndex")[-1].split(" ")[1]
            print("_________________________________________Country: ", country_name)
            country_list.append(country_name)
            country_dict[country_name] = pd.read_spss(pathname + filename)
        except: 
            pass
    # The output is a dictionary containing all 9 tables and their corresponding country. 
    return country_dict

def generating_final_tables(country_dict: dict) -> dict:
    # We initialize the DataFrames to use during the execution of the code
    main_ddbb = pd.DataFrame()
    answers_ddbb_regions = pd.DataFrame()
    GTP_ddbb_final = pd.DataFrame()
    main_ddbb_final = pd.DataFrame()

    for country, ddbb in country_dict.items():
        #__________________________________________________________________________MAIN DDBB
        # Structure to take
        str_main = structure_main.loc[:,["Name",country]].dropna()
        
        # We define the database with the main info
        main_ddbb = ddbb.loc[:,list(str_main[country].values)]
        
        #We add the country column
        main_ddbb["Country"] = country
        
        #************************************************* Headers name change
        old_names_main = main_ddbb.columns
        
        # Create a dictionary that maps the old names to the new names
        rename_dict = dict(zip(old_names_main, list(str_main["Name"].values)))

        # Rename the columns using the rename method
        main_ddbb.rename(columns=rename_dict, inplace=True)
        #*************************************************
        
        # Concatenating databases to merge a final main ddbb
        main_ddbb_final = pd.concat([main_ddbb_final, main_ddbb], ignore_index=True)

        #____________________________________________________________________________GLOBAL TRAVEL PROFILES 
        # Structure to take
        str_gen  = structure_generica.loc[:,["Name",country]].dropna()
        selector = list(str_gen[country].values)
        selector.insert(0,"caseid")

        # We define the database with the GTP info
        GTP_ddbb = ddbb.loc[:,selector]

        #************************************************* Headers name change
        headers_name_gen = list(str_gen["Name"].values)
        headers_name_gen.insert(0,"caseid")
        old_names_GPT = GTP_ddbb.columns

        # Create a dictionary that maps the old names to the new names
        rename_dict = dict(zip(old_names_GPT, headers_name_gen))

        # Rename the columns using the rename method
        GTP_ddbb.rename(columns=rename_dict, inplace=True)
        #*************************************************

        # Concatenating databases to merge a final main ddbb
        GTP_ddbb_final = pd.concat([GTP_ddbb_final, GTP_ddbb], ignore_index=True)
        
        #____________________________________________________________________________REGION ANSWERS
        #We iterate over all regions for each country
        for ii in list(set(structure_regions[["Dest",country]].dropna()["Dest"].values)):

            #We select the destination region
            current_data = structure_regions[structure_regions["Dest"]==ii]
            
            # We select the data to take
            selector  = current_data[country].dropna()
            selector = list(selector.values)
            selector.insert(0,"caseid")
            
            # Define the headers name
            headers_name_gen = list(str_gen["Name"].values)
            headers_name_gen.insert(0,"caseid")
            structure = current_data["Name"]
            
            # Define the database with the region info
            dest_ddbb = ddbb.loc[:,list(selector)]
            
            #************************************************* Headers name change
            
            # We add the region name
            dest_ddbb["Dest"] = Regions_dict[country][int(ii)]

            old_names = dest_ddbb.columns
            # Create a dictionary that maps the old names to the new names
            if len(old_names)<20:
                rename_dict = dict(zip(old_names, answer_region_heads_none_these))
            else:
                rename_dict = dict(zip(old_names, answer_region_heads))

            # Rename the columns using the rename method
            dest_ddbb.rename(columns=rename_dict, inplace=True)
            #*************************************************
            
            answers_ddbb_regions = pd.concat([answers_ddbb_regions, dest_ddbb]) 
    return {"main_ddbb_final": main_ddbb_final, "GTP_ddbb_final": GTP_ddbb_final, "answers_ddbb_regions": answers_ddbb_regions }

def save_tables(table_dict: dict):
    # Save all tables in a folder in CSV format
    table_dict["main_ddbb_final"].to_csv("Output/main_ddbb_"+Q+".csv")
    table_dict["GTP_ddbb_final"].to_csv("Output/GTP_ddbb_"+Q+".csv")
    table_dict["answers_ddbb_regions"].to_csv("Output/answers_ddbb_regions_"+Q+".csv")


if __name__ == "__main__":

    # We define the quarter
    Q = "Q3"

    # Define the pathname where our data is contained
    pathname = "Data/"+Q+"/"

    # Get the data
    data = get_data(pathname, Q)

    # Model the data
    tables = generating_final_tables(data)

    # Save the data into a CSV format
    save_tables(tables)