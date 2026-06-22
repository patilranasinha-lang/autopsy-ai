import logging
import pandas as pd
import io

logger = logging.getLogger(__name__)


class DataProcessorService:
    def __init__(self):
        pass
        
    def process_user_data(self, file):
        try:
            # Read the file into a DataFrame
            df = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
            
            summary = {
                "row_count": len(df),
                "columns": list(df.columns),
                "head": df.head(5).to_dict(orient='records')
            }
            
            logger.info(f'Successfully processed data, {len(df)} rows')
            return {"status": "success", "data": summary}
        except Exception as e:
            logger.error(f'Error processing data: {str(e)}')
            return {"status": "error", "message": str(e)}