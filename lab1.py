from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests as req

resp = req.get("https://kpfu.ru")
soup = BeautifulSoup(resp.text, 'lxml')
find_inst = soup.findAll('div', {'class': 'uk-accordion-content'})[10]
inst_list_url = [i.a['href'] for i in find_inst.findAll('div')]
inst_list = [[i.a.get_text().strip(), ] for i in find_inst.findAll('div')]
# print(inst_list)

menu_list = ['Структура', 'Об институте', 'Институт ', 'О нас']
kaf_list = ['Кафедра', 'Кафедpа', 'color: #012a77;font-size: 16px;font-weight: bold;text-decoration:none;', 'школа']
kol_list = ['Коллектив кафедры', 'Сотрудники', 'Состав', 'Список сотрудников']

for i in range(1):
        #range(len(inst_list_url)):
    if not ('Институт' in inst_list[i][0] or 'школа' in inst_list[i][0] or 'факультет' in inst_list[i][0]):
        continue
        inst_list[i].append([])
    cur_inst_site_url = inst_list_url[i]
    if 'geo.kpfu.ru' in cur_inst_site_url or 'www.kpfu.ru/main_page?p_sub=9072' in cur_inst_site_url:
        continue
    resp = req.get(cur_inst_site_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    left_menu = soup.findAll('ul', {'class': 'menu_list_left'})[0]
    inst_link_element = left_menu.find(lambda tag: tag.name == 'a' and (menu_list[0] in tag.text or menu_list[1] in tag.text or menu_list[2] in tag.text or menu_list[
        3] in tag.text))['href']
    struct_cur_inst_url = None
    if inst_link_element is not None:
        struct_cur_inst_url = inst_link_element
    print('Parsing ' + struct_cur_inst_url)
    if struct_cur_inst_url is None:
        inst_list[i].append([])
        continue
    resp = req.get(cur_inst_site_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    bs_cur_inst_kaf = soup.findAll(
        lambda tag: tag.name == 'a' and (kaf_list[0] in tag.text or kaf_list[1] in tag.text) or (
                tag.name == 'a' and tag.get('style') == kaf_list[2] and kaf_list[3] in tag.text))
    if not bs_cur_inst_kaf:
        try:
            bs_cur_inst_kaf = (BeautifulSoup(urlopen(bs_cur_inst_struct.find('ul', {'class': 'menu_list_left'}).find(
                lambda tag: tag.name == 'a' and 'Кафедры' in tag.text)['href']), "html.parser")).findAll(
                lambda tag: tag.name == 'a' and ('Кафедра' in tag.text))
        except:
            pass
    kaf_list_url = [[t.get_text().strip(), t.get('href')] for t in bs_cur_inst_kaf]
    for k in kaf_list_url:
        bs_kaf_page = BeautifulSoup(urlopen(k[1]), "html.parser")
        bs_kaf_kol_url = bs_kaf_page.find('ul', {'class': 'menu_list_left'}).find(lambda tag: tag.name == 'a' and (kol_list[0] in tag.text or kol_list[1] in tag.text or kol_list[2] in tag.text or kol_list[3] in tag.text))
        if bs_kaf_kol_url is not None:
            kaf_kol_url = bs_kaf_sostav_url['href']
        else:
            k.append(0)
            continue
        bs_kaf_kol_iframe = BeautifulSoup(urlopen(kaf_sostav_url), "html.parser").find('iframe')
        if bs_kaf_kol_iframe is None:
            k.append(0)
            continue
        kaf_kol_iframe_src = bs_kaf_sostav_iframe['src']
        bs_kaf_workers = BeautifulSoup(urlopen(kaf_sostav_iframe_src), "html.parser").findAll('span', {'class': 'fio'})
        kaf_workers_num = 0
        if bs_kaf_workers is not None:
            kaf_workers_num = len(bs_kaf_workers)
        k.append(kaf_workers_num)
    inst_list[i].append(kaf_list)

print(inst_list[0])
