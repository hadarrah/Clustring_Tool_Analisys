import pandas as pd


def export_document_distribution(xlsx_path, df_toExport, data):
    writer = pd.ExcelWriter(xlsx_path, engine='xlsxwriter')
    df_toExport.to_excel(writer, sheet_name="document_distribution")
    workbook = writer.book
    worksheet = writer.sheets["document_distribution"]
    chart = workbook.add_chart({'type': 'column'})
    # [sheetname, first_row, first_col, last_row, last_col].
    number_of_docs = len(data.get_documents_distribution_data()['Documents'])
    chart.add_series({
        'categories': ['document_distribution', 1, 1, number_of_docs, 1],
        'values': ['document_distribution', 1, 2, number_of_docs, 2],
        'gap': 2,
    })
    chart.set_title({'name': 'Document Distribution'})
    # Configure the chart axes.
    chart.set_y_axis({'major_gridlines': {'visible': False}})
    chart.set_y_axis({'name': 'Styles'})
    chart.set_x_axis({'name': 'Documents'})

    # Turn off chart legend. It is on by default in Excel.
    chart.set_legend({'position': 'none'})

    # Insert the chart into the worksheet.
    worksheet.insert_chart('D2', chart)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

def export_chunks_distribution(xlsx_path, df_toExport, data, doc):
    writer = pd.ExcelWriter(xlsx_path, engine='xlsxwriter')
    df_toExport.to_excel(writer, sheet_name="chunks_distribution")
    workbook = writer.book
    worksheet = writer.sheets["chunks_distribution"]
    chart = workbook.add_chart({'type': 'column'})
    # [sheetname, first_row, first_col, last_row, last_col].
    number_of_chunks = len(data.get_chunks_distribution_data(doc)['Chunks'])
    chart.add_series({
        'categories': ['chunks_distribution', 1, 1, number_of_chunks, 1],
        'values': ['chunks_distribution', 1, 2, number_of_chunks, 2],
        'gap': 2,
    })
    chart.set_title({'name': 'Chunks Distribution'})
    # Configure the chart axes.
    chart.set_y_axis({'major_gridlines': {'visible': False}})
    chart.set_y_axis({'name': 'Styles'})
    chart.set_x_axis({'name': 'Chunks'})

    # Turn off chart legend. It is on by default in Excel.
    chart.set_legend({'position': 'none'})

    # Insert the chart into the worksheet.
    worksheet.insert_chart('D2', chart)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

def export_zv_dependencies(xlsx_path, df_toExport, data, doc):
    writer = pd.ExcelWriter(xlsx_path, engine='xlsxwriter')
    df_toExport.to_excel(writer, sheet_name="zv dependencies")
    workbook = writer.book
    worksheet = writer.sheets["zv dependencies"]
    chart = workbook.add_chart({'type': 'line'})
    # [sheetname, first_row, first_col, last_row, last_col].
    number_of_chunks = len(data.get_zv_dependencies_data(doc)['Chunks'])
    chart.add_series({
        'categories': ['zv dependencies', 1, 1, number_of_chunks, 1],
        'values': ['zv dependencies', 1, 2, number_of_chunks, 2],
    })
    chart.set_title({'name': 'ZV Dependencies'})
    # Configure the chart axes.
    chart.set_y_axis({'major_gridlines': {'visible': False}})
    chart.set_y_axis({'name': 'ZV'})
    chart.set_x_axis({'name': 'Chunks', 'label_position': 'low'})

    # Turn off chart legend. It is on by default in Excel.
    chart.set_legend({'position': 'none'})

    # Insert the chart into the worksheet.
    worksheet.insert_chart('D2', chart)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()