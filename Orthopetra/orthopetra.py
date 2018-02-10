from collections import defaultdict
import matplotlib.pyplot as plt

def read_file(filename):
    read_data=open(filename, 'r')
    #contents=make_utf8(read_data.read()) #python2
    contents=read_data.read().encode('ascii', 'ignore').decode('ascii') #python3
    read_data.close()
    contents=contents.split('\n')
    return contents

def init_dictionary(num_fields):
    list_dict=[]
    while num_fields>1:
        list_dict.append(defaultdict(lambda:[]))
        num_fields-=1
    return list_dict

def get_authyr(values):
    values=values.strip('()')
    values=values.split(',')
    authors=[]
    n=len(values)
    year=int(values[n-1])
    for value in values[:n-1]:
        if '&' in value:
            value=value.split('&')
            authors.append(value[0].strip())
            authors.append(value[1].strip())
        else:
            authors.append(value.strip())
    return authors, year

def get_coauthors(author_list, author):
    coauthors=set()
    for authors in author_list:
        if authors!=author:
            coauthors.add(authors)
    return coauthors

def generate_dictionary(contents):
    ortho_list_dict=init_dictionary(len(contents[0].split(';')))
    for content in contents[1:]:
        values=content.split(';')
        family=values[0]
        genus=values[2]
        subgenus=values[3]
        species=values[4]        
        subspecies=values[5]
        author_list, year= get_authyr(values[6])
        ortho_list_dict[4][year].append((family, genus, subgenus, species, subspecies, author_list))
        for author in author_list:
            coauthors=get_coauthors(author_list, author)
            ortho_list_dict[3][author].append((family, genus, subgenus, species, subspecies, year, coauthors))
        ortho_list_dict[2][species].append((family,genus,subgenus,subspecies, author_list, year))
        ortho_list_dict[1][genus].append((family, subgenus, species, subspecies, author_list, year))
        ortho_list_dict[0][family].append((genus, subgenus, species, subspecies, author_list, year))
    return ortho_list_dict

def total_subspecies(species_dict):
    subspecies_set=set()
    for species, data_set in species_dict.items():
        for data_tuple in data_set:
            if data_tuple[3]:
                key=data_tuple[:-2]+(species,)
                subspecies_set.add(key)
    return len(subspecies_set)

def total_species(species_dict):
    species_set=set()
    for species, data_set in species_dict.items():
        for data_tuple in data_set:
            key=data_tuple[:3]+(species,)
            species_set.add(key)
    return len(species_set)

def num_species_subspecies(ortho_list_dict):
    num_species=total_species(ortho_list_dict[2])
    num_subspecies=total_subspecies(ortho_list_dict[2])
    total=num_species+num_subspecies
    print('Num species=', num_species,'\nNum subspecies=', num_subspecies)
    return total

def num_distinct_families(ortho_list_dict):
    return len(ortho_list_dict[0])

def min_max_kv(dictionary):
    min=list(dictionary.values())[0]
    max=min
    for key, value in dictionary.items():
        if value < min:
            min = value
        if value > max:
            max = value
    min_kv=[]
    max_kv=[]
    for key, value in dictionary.items():
        if value==min:
            min_kv.append((key, value))
        if value==max:
            max_kv.append((key, value))
    return min_kv, max_kv

def dict_type_count(dictionary, type):
    count_dict={}
    for key, data_list in dictionary.items():
        data_set=set()
        for data_tuple in data_list:
            if data_tuple[type]:
                data_set.add(data_tuple[:type+1])
        count_dict[key]=len(data_set)
    return min_max_kv(count_dict)

def in_between(lower, upper, val):
    return val>=lower and val<=upper

def compare_periods(period1, period2):
    check1=in_between(period2[0], period2[1], period1[0])
    check2=in_between(period2[0], period2[1], period1[1])
    check3=in_between(period1[0], period1[1], period2[0])
    check4=in_between(period1[0], period1[1], period2[1])
    return check1 or check2 or check3 or check4

def active_scientists(year_dict):
    active_dict=defaultdict(lambda: set())
    for author1, period1 in year_dict.items():
        for author2, period2 in year_dict.items():
            if author1!=author2 and compare_periods(period1, period2):
                    active_dict[author1].add((author2, period2))
    return active_dict

def author_queries(auth_dict):
    count_species_dict={}
    count_subspecies_dict={}
    coauth_dict={}
    year_dict=defaultdict(lambda: set())
    for author, data_list in auth_dict.items():
        species_set=set()
        subspecies_set=set()
        coauth_set=set()
        year_set=set()
        for data_tuple in data_list:
            species_set.add(data_tuple[:4])
            year_set.add(data_tuple[-2])
            if data_tuple[4]:
                subspecies_set.add(data_tuple[:5])
            for coauthors in data_tuple[6]:
                coauth_set.add(coauthors)
        count_species_dict[author]=len(species_set)
        count_subspecies_dict[author]=len(subspecies_set)
        coauth_dict[author]=coauth_set
        year_dict[author]=(min(year_set), max(year_set))
    return count_species_dict, count_subspecies_dict, coauth_dict, year_dict

def generate_scientific_names(data_set):
    names=[]
    for data in data_set:
        name=''
        for value in data:
            if value:
                name+=str(value)+' '
        names.append(name.strip())
    return names

def construct_authyr(auth_list, year):
    authyr=auth_list[0]
    n=len(auth_list)
    for author in auth_list[1:n-1]:
        authyr+=', '+author
    if n>1:
        authyr+=' & ' + auth_list[n-1]
    return authyr+', '+str(year)

def merge_fields(family_dict):
    merged_data=[]
    for record_list in family_dict.values():
        for tuples in record_list:
            data=tuples[0]+' '
            if tuples[1]:
                data+='('+tuples[1]+')'+ ' '
            data+=tuples[2]+' '
            if tuples[3]:
                data+=tuples[3] + ' '
            data+=construct_authyr(tuples[4], tuples[5])
            merged_data.append(data.strip())
    return merged_data

def write_to_file(data_list):
    fp=open('Outputs/merged.txt','w')
    for data in data_list:
        fp.write(data+'\n')
    fp.close()

def latest_species(year_dict):
    recent_year=max(year_dict.keys())
    species_set=set()
    for data_tuple in year_dict[recent_year]:
        species_set.add(data_tuple[:4])
    return recent_year, generate_scientific_names(species_set)

def year_species_count(year_dict):
    count_species_dict={}
    for year, data_list in year_dict.items():
        species_set=set()
        for data_tuple in data_list:
            species_set.add(data_tuple[3:5])
        count_species_dict[year]=len(species_set)
    return count_species_dict

def show_hist(count_dict):
    years=list(count_dict.keys())
    species=list(count_dict.values())
    plt.bar(years,species)
    plt.xlabel('Year')
    plt.ylabel('Num_Species_Discovered')
    plt.title('Yearwise Species Histogram')
    plt.show()

contents=read_file('orthoptera.txt')
ortho_list_dict=generate_dictionary(contents)

print('Total=', num_species_subspecies(ortho_list_dict))
print('\nNum Distinct families=', num_distinct_families(ortho_list_dict))
print('\nFamily with the most_species=', dict_type_count(ortho_list_dict[0], 2)[1])
print('\nGenus with the most subspecies=', dict_type_count(ortho_list_dict[1], 3)[1])

#author='Heller'
author='Linnaeus'
authdict=author_queries(ortho_list_dict[3])
print('\nNum species described by '+ author +'=', authdict[0][author])
print('Num subspecies described by '+ author +'=', authdict[1][author])
print('Coauthors of '+ author +'=', authdict[2][author])
print('Active period:', authdict[3][author])
print('Other active scientists during this period:', active_scientists(authdict[3])[author])

author='F. Willemse'
#author='di Mauro'
print('\nNum species described by '+ author +'=', authdict[0][author])
print('Num subspecies described by '+ author +'=', authdict[1][author])
print('Coauthors of '+ author +'=', authdict[2][author])

recent_year, species=latest_species(ortho_list_dict[4])
print('\nRecently discovered species('+str(recent_year)+'):', species)

write_to_file(merge_fields(ortho_list_dict[0]))

yr_spec=year_species_count(ortho_list_dict[4])
print('Lowest species count in year: ', min_max_kv(yr_spec)[0])
print('Highest species count in year: ', min_max_kv(yr_spec)[1])
show_hist(yr_spec)
