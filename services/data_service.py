"""
Servicio de integración entre Pandas y PostgreSQL
Combina procesamiento de datos con acceso a base de datos
"""
from services.data_processor import DataProcessor
from database import Query
from typing import Dict, Any, List
import pandas as pd


class DataService:
    """
    Servicio que integra procesamiento de datos (Pandas) con PostgreSQL
    """
    
    def __init__(self):
        self.processor = DataProcessor()
        self.query = Query()
    
    def load_and_process_from_db(self, function_name: str, params: Dict = None) -> pd.DataFrame:
        """
        Carga datos desde PostgreSQL y los convierte a DataFrame
        
        Args:
            function_name: Nombre de la función PostgreSQL
            params: Parámetros para la función
        
        Returns:
            DataFrame con los datos procesados
        
        Example:
            service = DataService()
            df = service.load_and_process_from_db('catalogomomentotomamuestra', {})
        """
        params = params or {}
        
        # Ejecutar query
        result = self.query.sp_execute(params, function_name)
        
        # Convertir a DataFrame
        df = self.processor.load_from_database(result)
        
        return df
    
    def process_and_save_to_db(
        self, 
        df: pd.DataFrame, 
        function_name: str,
        batch_size: int = 100
    ) -> List[Dict]:
        """
        Procesa DataFrame y guarda en PostgreSQL
        
        Args:
            df: DataFrame a procesar
            function_name: Función PostgreSQL para insertar
            batch_size: Tamaño del lote para inserciones
        
        Returns:
            Lista de resultados de las inserciones
        
        Example:
            results = service.process_and_save_to_db(
                df, 
                'ins_glucose_record',
                batch_size=50
            )
        """
        results = []
        records = df.to_dict(orient='records')
        
        # Insertar en lotes
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            
            for record in batch:
                try:
                    result = self.query.sp_execute(record, function_name)
                    results.append({
                        'success': True,
                        'record': record,
                        'result': result
                    })
                except Exception as e:
                    results.append({
                        'success': False,
                        'record': record,
                        'error': str(e)
                    })
        
        return results
    
    def aggregate_and_save(
        self,
        function_name: str,
        params: Dict,
        group_by: List[str],
        agg_dict: Dict[str, str],
        save_function: str
    ) -> Dict[str, Any]:
        """
        Pipeline completo: Carga -> Agrega -> Guarda
        
        Example:
            result = service.aggregate_and_save(
                function_name='get_glucose_records',
                params={'user_id': 1},
                group_by=['moment_id'],
                agg_dict={'glucose_value': 'mean'},
                save_function='save_aggregated_data'
            )
        """
        # 1. Cargar datos
        df = self.load_and_process_from_db(function_name, params)
        
        # 2. Agregar
        aggregated = df.groupby(group_by).agg(agg_dict).reset_index()
        
        # 3. Guardar
        results = self.process_and_save_to_db(aggregated, save_function)
        
        return {
            'original_rows': len(df),
            'aggregated_rows': len(aggregated),
            'saved_results': results
        }
    
    def analyze_glucose_patterns(self, user_id: int) -> Dict[str, Any]:
        """
        Ejemplo específico: Analizar patrones de glucosa de un usuario
        
        Args:
            user_id: ID del usuario
        
        Returns:
            Análisis estadístico de glucosa
        """
        # Cargar datos del usuario
        df = self.load_and_process_from_db(
            'get_user_glucose_records',
            {'user_id': user_id}
        )
        
        if df.empty:
            return {'error': 'No hay datos para este usuario'}
        
        # Análisis
        analysis = {
            'user_id': user_id,
            'total_records': len(df),
            'average_glucose': float(df['glucose_value'].mean()),
            'min_glucose': float(df['glucose_value'].min()),
            'max_glucose': float(df['glucose_value'].max()),
            'std_glucose': float(df['glucose_value'].std()),
            'by_moment': df.groupby('moment_id')['glucose_value'].mean().to_dict()
        }
        
        return analysis


# ============ EJEMPLO DE USO ============

def ejemplo_uso_completo():
    """Ejemplo de uso completo del servicio"""
    service = DataService()
    
    # 1. Cargar catálogo desde PostgreSQL
    print("1. Cargando catálogo de momentos...")
    df_moments = service.load_and_process_from_db('catalogomomentotomamuestra', {})
    print(df_moments)
    
    # 2. Procesar datos con pandas
    print("\n2. Procesando datos...")
    df_moments['active'] = True
    df_moments['priority'] = range(1, len(df_moments) + 1)
    
    # 3. Analizar patrones
    print("\n3. Analizando patrones de glucosa del usuario 1...")
    analysis = service.analyze_glucose_patterns(user_id=1)
    print(analysis)
    
    print("\n✓ Pipeline completado")


if __name__ == '__main__':
    ejemplo_uso_completo()
