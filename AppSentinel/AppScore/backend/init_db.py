from services.app_catalog import AppCatalogService

def main():
    # Initialize app catalog service
    app_catalog = AppCatalogService()
    
    # Add test data
    app_catalog.add_test_data()
    
    print("Database initialized with test data!")

if __name__ == "__main__":
    main()
