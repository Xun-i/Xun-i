def pandas_(exc_,sheet_name):
  df = pd.read_excel(exc_, sheet_name=sheet_name, keep_default_na=False)
  skus = sku_data = []
  for dat in df.values:
      skus.append(dat[0])
      sku_data.append([data for data in dat[18:] if sku != ''])

def openpyxl_(exc_,sheet_name):
  workbook = ol.load_workbook(os.path.join(exc_), data_only=True)
  table = workbook.active
  table = workbook[sheet_name]  # 选择表
  row = 3
  for data in OA:
      table[f'A{row}'] = 'value'  # 插值
      row = row + 1
  workbook.save(exc_)  # 保存
