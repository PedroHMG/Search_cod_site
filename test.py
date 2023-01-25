from flask import Flask, render_template, request
import pandas as pd

x = pd.read_csv('temp_data.csv')

print(x.to_dict('list'))
