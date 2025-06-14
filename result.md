# Local Test Result

We executed `python app.py` using the provided sample sales data and the question:
"3年間の各商品の平均売上個数から、翌年の入荷数を予測してください。"

The script returned a dataframe with predicted stock numbers for each product, as shown below (truncated):

```
    product_name  product_id  predicted_stock
0          商品001           1        20.322404
1          商品002           2        19.775956
...
299        商品300         300        20.158470
```

The OPENAI_API_KEY environment variable was used to access the OpenAI API during the test.

## Consistency Check
We inspected `sample_sales.csv` and found that the data only contains sales for
the year 2024. Because the dataset lacks three full years of history, the
predicted stock levels produced by PandasAI may not be a reliable estimate of
future inventory needs.
