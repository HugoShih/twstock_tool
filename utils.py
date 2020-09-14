from datetime import timedelta, date
import streamlit as st
import pandas as pd

# create date range
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)



