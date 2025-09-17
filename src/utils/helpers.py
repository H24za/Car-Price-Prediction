import pandas as pd
import numpy as np
from typing import Tuple, List


def ensure_numeric_splits(X_train: pd.DataFrame, X_val: pd.DataFrame, X_test: pd.DataFrame = None,
						  fill_value: float = None) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
	"""Coerce object columns to numeric across train/val/test and impute missing values using train medians.

	Returns the (X_train, X_val, X_test) tuple where all columns are numeric dtype and NaNs filled.
	"""
	X_train = X_train.copy()
	X_val = X_val.copy()
	X_test = X_test.copy() if X_test is not None else None

	# coerce object-like columns to numeric
	for df in (X_train, X_val) if X_test is None else (X_train, X_val, X_test):
		for col in df.select_dtypes(include=['object', 'category']).columns:
			df[col] = pd.to_numeric(df[col], errors='coerce')

	# compute medians from train
	medians = X_train.median(numeric_only=True)
	if fill_value is None:
		fill_values = medians.to_dict()
	else:
		fill_values = {c: fill_value for c in X_train.columns}

	X_train = X_train.fillna(fill_values)
	X_val = X_val.fillna(fill_values)
	if X_test is not None:
		X_test = X_test.fillna(fill_values)

	# After fill, ensure numeric dtypes
	for df in (X_train, X_val) if X_test is None else (X_train, X_val, X_test):
		for col in df.columns:
			if df[col].dtype == 'object':
				df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

	return X_train, X_val, X_test
