import pandas as pd
from flask import Flask, render_template, request, session, send_file, url_for
from flask_sqlalchemy import SQLAlchemy
from search_service_cod import search_with_name, search_with_cnpj
from search_item_cod import search_item_data, data_read
from os import path
import numpy as np



app = Flask(__name__)
app.secret_key =  'hello'

data = pd.read_csv('Data\Service_data.csv')
data = data.drop("Unnamed: 0", axis=1)

item_data = data_read(r'Data\Planilha_de_itens.xlsx')
pick_data = pd.DataFrame()

temp_data_path = 'Data\temp_data.csv'
header_list = ['FILIAL', 'DESC ITEM', 'COD ITEM'] 
df = pd.DataFrame(columns=header_list)
df.to_csv("temp_data.csv", index=False)




@app.route('/codigo_servico')
def csvtohtml():
    return render_template('index.html',  tables=[data.to_html(classes='data')], titles=data.columns.values)



@app.route('/codigo_servico', methods=['POST'])
def form_service():
    supply_name = request.form['search_name']
    supply_cnpj = request.form['search_cnpj']
    
    if supply_name:
        supply_name = supply_name.upper()
        show_data = search_with_name(supply_name)
        
        return render_template('index.html',  tables=[show_data.to_html(classes='data')], titles=data.columns.values)
    else:
        show_data = search_with_cnpj(supply_cnpj)
        return render_template('index.html',  tables=[show_data.to_html(classes='data')], titles=data.columns.values)


@app.route('/codigo_item', methods=['GET', 'POST'])
def form_iten():
    if request.method == 'POST':
        if 'search_name' in request.form:
            item_name = request.form['search_name']
            item_name = item_name.upper()
            show_data = search_item_data(item_data, item_name)
            session['search_data'] = show_data.to_dict('list')

            show_selection = pd.DataFrame(session['selected_data'])
            show_selection = show_selection[['index', 'DESC ITEM', 'COD ITEM']]

            return render_template("Item_search.html", column_names=show_data.columns.values, row_data=list(show_data.values.tolist()), 
                            row_selected=list(show_selection.values.tolist()), link_column='COD ITEM', zip=zip)

        elif request.form.get('row_id'):
            item_row = int(request.form.get('row_id'))
            show_data = pd.DataFrame(session['search_data'])
            show_data = show_data[['index', 'DESC ITEM', 'COD ITEM']]
            add_row = show_data.loc[show_data['COD ITEM'] == item_row]
            add_row = add_row.iloc[[0]]
            

            temp_data = pd.DataFrame(session['selected_data'])
            temp_data = pd.concat([add_row, temp_data])
            session['selected_data'] = temp_data.to_dict('list')
            
            add_row.to_csv('temp_data.csv', mode='a', index=False, header=False)
            print(pd.DataFrame(session['selected_data']))

            show_selection = pd.DataFrame(session['selected_data'])
            show_selection = show_selection[['index', 'DESC ITEM', 'COD ITEM']]
            show_selection['COD ITEM'] = show_selection['COD ITEM'].astype(np.int64)
            
            return render_template("Item_search.html", column_names=show_data.columns.values, row_data=list(show_data.values.tolist()), 
                            row_selected=list(show_selection.values.tolist()), link_column='COD ITEM', zip=zip)
        
        elif request.form.get('export'):
            return render_template('index.html',  tables=[data.to_html(classes='data')], titles=data.columns.values)

        

    elif request.method == 'GET':
        session['selected_data'] = {'index': [], 'DESC ITEM': [], 'COD ITEM': []}
        session['search_data'] = []
        return render_template('item_search.html',  tables=[data.to_html(classes='data')], titles=data.columns.values)


@app.route('/download')
def download_file():
    export_file = pd.DataFrame(session['selected_data'])
    export_file = export_file[['index', 'DESC ITEM', 'COD ITEM']]
    export_file['COD ITEM'] = export_file['COD ITEM'].astype(np.int64)
    export_file.to_csv("temp_data.csv", index=False)
    mimetype='temp_data/csv'
    return send_file("temp_data.csv", as_attachment=True)




if __name__ == '__main__':
    app.secret_key =  'hello'
    app.run(debug=True)