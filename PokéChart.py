#!/usr/bin/env python
# coding: utf-8

# In[265]:


import requests as req
import csv, json


# In[266]:


url_group = []
resp_group = []
raw_data_group = []
final_data_group = [["Tipo", "Quantidade"]]
for url in range(18):
    url_group.append("https://pokeapi.co/api/v2/type/" + str(url+1))
    resp_group.append(req.get(url_group[url]))
    raw_data_group.append(resp_group[url].json())
    final_data_group.append([raw_data_group[url]["name"], len(raw_data_group[url]["pokemon"])])


# In[267]:


with open("pokechart.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerows(final_data_group)


# In[268]:


def get_pokechart_data(csv_path, json_path):
    data = {}
    with open(csv_path, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for rows in reader:
            id = rows['Tipo']
            data[id] = rows
    with open(json_path, "w") as json_file:
        json_file.write(json.dumps(data, indent=2))
    with open(json_path, "r") as json_file:
        data = json.load(json_file)
    return data


# In[269]:


def get_x_labels(data):
    labels = []
    for t in range(0, len(data)):
        labels.append(list(data)[t])
    return labels


# In[294]:


def get_data_amounts(data):
    indexes = []
    amounts = []
    for t in range(0, len(data)):
        indexes.append(list(data)[t])
    for key in indexes:
        amounts.append(data[key]["Quantidade"])
    return amounts


# In[295]:


def set_data_backgrounds():
    colors = [
        "rgba(170, 176, 159, 1)",
        "rgba(203, 95, 72, 1)",
        "rgba(125, 166, 222, 1)",
        "rgba(180, 104, 183, 1)",
        "rgba(204, 159, 79, 1)",
        "rgba(178, 160, 97, 1)",
        "rgba(148, 188, 74, 1)",
        "rgba(132, 106, 182, 1)",
        "rgba(137, 161, 176, 1)",
        "rgba(234, 122, 60, 1)",
        "rgba(83, 154, 226, 1)",
        "rgba(113, 197, 88, 1)",
        "rgba(229, 197, 49, 1)",
        "rgba(229, 112, 155, 1)",
        "rgba(112, 203, 212, 1)",
        "rgba(106, 123, 175, 1)",
        "rgba(115, 108, 117, 1)",
        "rgba(227, 151, 209, 1)"
    ]
    return colors


# In[348]:


def set_chart(labels, amounts, colors, title="Meu Gráfico", type="bar"):    
    data = []
    for n in range(0, len(labels)):
        data.append(amounts[n])
    chart = {
        "type": type,
        "data": {
            "labels": labels,
            "datasets": [{
                "label": "",
                "data": data,
                "backgroundColor": colors
            }]
        },
        "options": {
            "legend": {
                "labels": {
                    "boxWidth": 0
                }
            },
            "title": {
                "display": "true",
                "text": title
            }
        }
    }
    return chart


# In[349]:


def get_api_chart(chart):
    url_base = "https://quickchart.io/chart"
    response = req.get(f"{url_base}?c={str(chart)}")
    return response.content


# In[350]:


def save_image(path, content):
    with open(path, "wb") as img:
        img.write(content)


# In[351]:


csv_path = "pokechart.csv"
json_path = "pokechart.json"
data = get_pokechart_data(csv_path, json_path)
labels = get_data_labels(data)
amounts = get_data_amounts(data)
colors = set_data_backgrounds()
chart = set_chart(labels, amounts, colors, title="Quantidade de Pokémon por Tipo")
content = get_api_chart(chart)
save_image("pokechart.png", content)

