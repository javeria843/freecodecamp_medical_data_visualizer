import medical_data_visualizer
medical_data_visualizer.draw_cat_plot().savefig("catplot.png")
medical_data_visualizer.draw_heat_map().savefig("heatmap.png")
import pandas as pd

df = pd.read_csv("medical_data.csv", delimiter=';')  # or ',' if comma-separated
print("✅ Columns:", df.columns.tolist())
print(df.head())

