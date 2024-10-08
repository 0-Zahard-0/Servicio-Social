import pandas as pd
import numpy as np
import utilities as util
import sys

#! COMMAND: python main.py "carga siia 232.xlsx" "CH 2023-2.xlsx"

def main():
    try:
        siiaPath = sys.argv[1]
        chPath = sys.argv[2]

        # file reading
        siia = util.read_siia(siiaPath)
        ch = util.read_ch(chPath)
        siia = util.change_col_order(siia)
        siia.insert(0, "div", "")

        # highlighting
        dfp = util.highlight_differences(siia, ch)
        dfp.data = util.insert_na(dfp.data)

        dfp.set_properties(**{
                'border': '1px solid black',
                'text-align': 'center'
            })

        writer = pd.ExcelWriter('comparasion.xlsx', engine='xlsxwriter')

        dfp.to_excel(writer, sheet_name='Sheet1', index=False)

        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        format_black = workbook.add_format({'bg_color': '#000000'})

        for row in range(1, len(dfp.data) + 1):  # Comienza en la fila 1
            worksheet.write_blank(row, dfp.data.columns.get_loc('div'), None, format_black)  # Columna 1 

        for i, col in enumerate(dfp.data.columns):
            max_len = max(dfp.data[col].apply(lambda x: len(str(x))).max(), len(col))
            worksheet.set_column(i, i, max_len + 1)

        writer.close()    

        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__=="__main__":
    main()