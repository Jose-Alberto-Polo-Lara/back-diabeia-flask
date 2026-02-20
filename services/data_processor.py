"""
Procesamiento de datasets con Pandas
Ejemplo de análisis y transformación de datos
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any
import json


class DataProcessor:
    """
    Clase para procesar datasets con pandas
    """
    
    def __init__(self):
        self.df = None
    
    # ============ CARGA DE DATOS ============
    
    def load_from_csv(self, filepath: str, **kwargs) -> pd.DataFrame:
        """
        Carga datos desde un archivo CSV
        
        Args:
            filepath: Ruta al archivo CSV
            **kwargs: Parámetros adicionales para pd.read_csv
        
        Returns:
            DataFrame con los datos cargados
        """
        self.df = pd.read_csv(filepath, **kwargs)
        print(f"✓ Dataset cargado: {self.df.shape[0]} filas, {self.df.shape[1]} columnas")
        return self.df
    
    def load_from_excel(self, filepath: str, sheet_name: str = 0) -> pd.DataFrame:
        """Carga datos desde un archivo Excel"""
        self.df = pd.read_excel(filepath, sheet_name=sheet_name)
        print(f"✓ Dataset cargado: {self.df.shape[0]} filas, {self.df.shape[1]} columnas")
        return self.df
    
    def load_from_json(self, filepath: str) -> pd.DataFrame:
        """Carga datos desde un archivo JSON"""
        self.df = pd.read_json(filepath)
        print(f"✓ Dataset cargado: {self.df.shape[0]} filas, {self.df.shape[1]} columnas")
        return self.df
    
    def load_from_dict(self, data: Dict[str, List]) -> pd.DataFrame:
        """Carga datos desde un diccionario"""
        self.df = pd.DataFrame(data)
        print(f"✓ Dataset creado: {self.df.shape[0]} filas, {self.df.shape[1]} columnas")
        return self.df
    
    def load_from_database(self, query_result: Dict[str, Any]) -> pd.DataFrame:
        """
        Carga datos desde el resultado de una query PostgreSQL
        
        Args:
            query_result: Resultado de query.sp_execute() con 'recordsets'
        
        Returns:
            DataFrame con los datos
        """
        if query_result.get('recordsets'):
            self.df = pd.DataFrame(query_result['recordsets'])
            print(f"✓ Dataset cargado desde BD: {self.df.shape[0]} filas, {self.df.shape[1]} columnas")
            return self.df
        else:
            raise ValueError("No hay datos en recordsets")
    
    # ============ ANÁLISIS EXPLORATORIO ============
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Obtiene un resumen del dataset
        
        Returns:
            Diccionario con estadísticas del dataset
        """
        if self.df is None:
            raise ValueError("No hay dataset cargado")
        
        summary = {
            'shape': self.df.shape,
            'columns': self.df.columns.tolist(),
            'dtypes': self.df.dtypes.astype(str).to_dict(),
            'missing_values': self.df.isnull().sum().to_dict(),
            'duplicates': int(self.df.duplicated().sum()),
            'memory_usage': f"{self.df.memory_usage(deep=True).sum() / 1024**2:.2f} MB"
        }
        
        return summary
    
    def get_statistics(self) -> pd.DataFrame:
        """Obtiene estadísticas descriptivas del dataset"""
        if self.df is None:
            raise ValueError("No hay dataset cargado")
        
        return self.df.describe(include='all')
    
    def show_info(self):
        """Muestra información del dataset"""
        if self.df is None:
            raise ValueError("No hay dataset cargado")
        
        print("\n" + "="*50)
        print("INFORMACIÓN DEL DATASET")
        print("="*50)
        print(f"Filas: {self.df.shape[0]}")
        print(f"Columnas: {self.df.shape[1]}")
        print(f"\nPrimeras 5 filas:")
        print(self.df.head())
        print(f"\nTipos de datos:")
        print(self.df.dtypes)
        print(f"\nValores nulos:")
        print(self.df.isnull().sum())
        print("="*50 + "\n")
    
    # ============ LIMPIEZA DE DATOS ============
    
    def remove_duplicates(self, subset=None, keep='first') -> pd.DataFrame:
        """
        Elimina filas duplicadas
        
        Args:
            subset: Columnas específicas para verificar duplicados
            keep: 'first', 'last' o False
        """
        original_count = len(self.df)
        self.df = self.df.drop_duplicates(subset=subset, keep=keep)
        removed = original_count - len(self.df)
        print(f"✓ Eliminadas {removed} filas duplicadas")
        return self.df
    
    def handle_missing_values(self, strategy='drop', fill_value=None) -> pd.DataFrame:
        """
        Maneja valores faltantes
        
        Args:
            strategy: 'drop', 'fill', 'ffill', 'bfill', 'mean', 'median'
            fill_value: Valor para rellenar (si strategy='fill')
        """
        if strategy == 'drop':
            self.df = self.df.dropna()
            print("✓ Filas con valores nulos eliminadas")
        elif strategy == 'fill':
            self.df = self.df.fillna(fill_value)
            print(f"✓ Valores nulos rellenados con {fill_value}")
        elif strategy == 'ffill':
            self.df = self.df.fillna(method='ffill')
            print("✓ Valores nulos rellenados con valor anterior")
        elif strategy == 'bfill':
            self.df = self.df.fillna(method='bfill')
            print("✓ Valores nulos rellenados con valor siguiente")
        elif strategy == 'mean':
            self.df = self.df.fillna(self.df.mean(numeric_only=True))
            print("✓ Valores nulos rellenados con la media")
        elif strategy == 'median':
            self.df = self.df.fillna(self.df.median(numeric_only=True))
            print("✓ Valores nulos rellenados con la mediana")
        
        return self.df
    
    def filter_data(self, condition) -> pd.DataFrame:
        """
        Filtra datos según una condición
        
        Example:
            processor.filter_data(processor.df['age'] > 18)
        """
        self.df = self.df[condition]
        print(f"✓ Dataset filtrado: {len(self.df)} filas restantes")
        return self.df
    
    # ============ TRANSFORMACIONES ============
    
    def add_calculated_column(self, column_name: str, calculation) -> pd.DataFrame:
        """
        Añade una columna calculada
        
        Example:
            processor.add_calculated_column('total', lambda df: df['price'] * df['quantity'])
        """
        self.df[column_name] = calculation(self.df)
        print(f"✓ Columna '{column_name}' añadida")
        return self.df
    
    def rename_columns(self, mapping: Dict[str, str]) -> pd.DataFrame:
        """Renombra columnas"""
        self.df = self.df.rename(columns=mapping)
        print(f"✓ Columnas renombradas: {list(mapping.keys())}")
        return self.df
    
    def convert_types(self, type_mapping: Dict[str, str]) -> pd.DataFrame:
        """
        Convierte tipos de datos
        
        Example:
            processor.convert_types({'date': 'datetime64', 'price': 'float'})
        """
        for col, dtype in type_mapping.items():
            if col in self.df.columns:
                if dtype == 'datetime64':
                    self.df[col] = pd.to_datetime(self.df[col])
                else:
                    self.df[col] = self.df[col].astype(dtype)
        
        print(f"✓ Tipos convertidos: {list(type_mapping.keys())}")
        return self.df
    
    # ============ AGREGACIONES ============
    
    def group_and_aggregate(self, group_by: List[str], agg_dict: Dict[str, str]) -> pd.DataFrame:
        """
        Agrupa y aplica funciones de agregación
        
        Example:
            processor.group_and_aggregate(
                group_by=['category'],
                agg_dict={'price': 'mean', 'quantity': 'sum'}
            )
        """
        result = self.df.groupby(group_by).agg(agg_dict).reset_index()
        print(f"✓ Agregación completada: {len(result)} grupos")
        return result
    
    def pivot_table(self, index, columns, values, aggfunc='mean') -> pd.DataFrame:
        """Crea una tabla pivote"""
        result = pd.pivot_table(
            self.df,
            index=index,
            columns=columns,
            values=values,
            aggfunc=aggfunc
        )
        print("✓ Tabla pivote creada")
        return result
    
    # ============ EXPORTACIÓN ============
    
    def export_to_csv(self, filepath: str, index=False) -> None:
        """Exporta a CSV"""
        self.df.to_csv(filepath, index=index)
        print(f"✓ Dataset exportado a {filepath}")
    
    def export_to_excel(self, filepath: str, sheet_name='Sheet1', index=False) -> None:
        """Exporta a Excel"""
        self.df.to_excel(filepath, sheet_name=sheet_name, index=index)
        print(f"✓ Dataset exportado a {filepath}")
    
    def export_to_json(self, filepath: str, orient='records') -> None:
        """Exporta a JSON"""
        self.df.to_json(filepath, orient=orient, indent=2)
        print(f"✓ Dataset exportado a {filepath}")
    
    def to_dict(self, orient='records') -> List[Dict]:
        """Convierte a lista de diccionarios"""
        return self.df.to_dict(orient=orient)
    
    def to_database_format(self) -> List[Dict]:
        """
        Convierte el DataFrame a formato para insertar en PostgreSQL
        
        Returns:
            Lista de diccionarios compatible con query.sp_execute()
        """
        return self.df.to_dict(orient='records')


# ============ EJEMPLOS DE USO ============

def ejemplo_datos_glucosa():
    """Ejemplo: Procesar datos de registros de glucosa"""
    print("\n" + "="*60)
    print("EJEMPLO: PROCESAMIENTO DE DATOS DE GLUCOSA")
    print("="*60)
    
    processor = DataProcessor()
    
    # Crear dataset de ejemplo
    data = {
        'user_id': [1, 1, 1, 2, 2, 2, 3, 3],
        'glucose_value': [120, 135, 110, 95, 140, 105, 130, 115],
        'moment_id': [1, 2, 3, 1, 2, 3, 1, 2],
        'date': pd.date_range('2024-02-01', periods=8, freq='D')
    }
    
    df = processor.load_from_dict(data)
    processor.show_info()
    
    # Calcular promedio por usuario
    print("\n📊 Promedio de glucosa por usuario:")
    result = processor.group_and_aggregate(
        group_by=['user_id'],
        agg_dict={'glucose_value': 'mean'}
    )
    print(result)
    
    # Filtrar valores altos
    print("\n⚠️ Valores de glucosa mayores a 120:")
    high_glucose = processor.filter_data(processor.df['glucose_value'] > 120)
    print(high_glucose)
    
    return processor


def ejemplo_integracion_postgresql():
    """Ejemplo: Integración con PostgreSQL"""
    print("\n" + "="*60)
    print("EJEMPLO: INTEGRACIÓN CON POSTGRESQL")
    print("="*60)
    
    # Simular resultado de PostgreSQL
    query_result = {
        'error': None,
        'excepcion': None,
        'recordsets': [
            {'id': 1, 'name': 'Ayuno', 'description': 'Antes del desayuno'},
            {'id': 2, 'name': 'Postprandial', 'description': 'Después de comida'},
            {'id': 3, 'name': 'Noche', 'description': 'Antes de dormir'}
        ]
    }
    
    processor = DataProcessor()
    df = processor.load_from_database(query_result)
    
    print("\n📋 Datos cargados desde PostgreSQL:")
    print(df)
    
    # Procesar y preparar para insertar
    df['active'] = True
    df['created_at'] = datetime.now()
    
    print("\n✅ Datos procesados listos para insertar:")
    print(df)
    
    # Convertir a formato para PostgreSQL
    records_to_insert = processor.to_database_format()
    print(f"\n📤 {len(records_to_insert)} registros listos para insertar en BD")
    
    return processor


if __name__ == '__main__':
    print("\n🐼 PROCESAMIENTO DE DATASETS CON PANDAS\n")
    
    # Ejecutar ejemplos
    ejemplo_datos_glucosa()
    ejemplo_integracion_postgresql()
    
    print("\n" + "="*60)
    print("✓ Ejemplos completados")
    print("="*60 + "\n")
