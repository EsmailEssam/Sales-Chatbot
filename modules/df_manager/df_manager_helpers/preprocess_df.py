import pandas as pd


class PreprocessDf:
    """Class to preprocess and enhance product DataFrame."""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize with input DataFrame."""
        self.df = df.copy()
        
    def _flatten_list(self, nested_list):
        """Flatten nested lists while preserving strings."""
        if isinstance(nested_list, list):
            if not nested_list:
                return []
            elif all(isinstance(item, str) for item in nested_list):
                return nested_list
            else:
                return [item for sublist in nested_list for item in (sublist if isinstance(sublist, list) else [sublist])]
        return nested_list

    def _preprocess_dataframe(self):
        """Preprocess the DataFrame with basic cleaning and transformations."""
        # Handle nested lists
        if 'concerns' in self.df.columns:
            self.df['concerns'] = self.df['concerns'].apply(self._flatten_list)
            self.df['concerns'] = self.df['concerns'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
        
        if 'ingredients' in self.df.columns:
            self.df['ingredients'] = self.df['ingredients'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
            
        if 'category' in self.df.columns:
            self.df['category'] = self.df['category'].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)
        
        # Clean text fields
        text_columns = ['name', 'description']
        for col in text_columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].str.replace(r'\s+', ' ', regex=True)
                self.df[col] = self.df[col].str.replace(r'\r\n', ' ', regex=True)
                self.df[col] = self.df[col].str.strip()
        
        # Extract short description
        if 'description' in self.df.columns:
            self.df['short_description'] = self.df['description'].apply(
                lambda x: x[:100] + '...' if isinstance(x, str) and len(x) > 100 else x
            )
        
        # Convert price to numeric
        if 'price' in self.df.columns:
            self.df['price'] = pd.to_numeric(self.df['price'], errors='coerce')
        
        # Handle None values
        self.df = self.df.fillna(value={
            'product_file': 'No file',
            'ingredients': 'Not specified',
            'concerns': 'Not specified'
        })
        
        # Extract parentheses content from name
        if 'name' in self.df.columns:
            self.df['name_attributes'] = self.df['name'].str.extract(r'\((.*?)\)', expand=False)
            self.df['clean_name'] = self.df['name'].str.replace(r'\s*\(.*?\)\s*', ' ', regex=True).str.strip()
        
        return self.df

    def _create_keyword_columns(self):
        """Create additional columns for enhanced searching."""
        # Create combined search text column
        self.df['search_text'] = (
            self.df['clean_name'].fillna('') + ' ' + 
            self.df['description'].fillna('') + ' ' + 
            self.df['ingredients'].fillna('') + ' ' + 
            self.df['concerns'].fillna('') + ' ' + 
            self.df['category'].fillna('')
        )
        
        # Convert to lowercase
        self.df['search_text'] = self.df['search_text'].str.lower()
        
        # Create price ranges
        if 'price' in self.df.columns:
            bins = [0, 50, 100, 200, 500, float('inf')]
            labels = ['0-50', '51-100', '101-200', '201-500', '500+']
            self.df['price_range'] = pd.cut(self.df['price'], bins=bins, labels=labels, right=False)
        
        return self.df

    def run(self) -> pd.DataFrame:
        """Execute full preprocessing pipeline and return enhanced DataFrame."""
        self._preprocess_dataframe()
        self._create_keyword_columns()
        return self.df