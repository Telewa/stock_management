# Stock Management System

One of the main challenges of building an ecommerce platform is to keep an accurate list of products and their stocks up to date.

Based on that, this is a system that allows us to manage products for an hypothetical ecommerce platform.

For this system a product has an unique SKU and could be commercialized in multiple countries. Each product can then have different stock per country.

It manages products and their stock with the following requirements:

1. It has a products API that allows:
   1. Get a product by SKU
      - URL: https://github.com/Telewa/stock_management/blob/master/apps_dir/product/urls.py#L6
      - View: https://github.com/Telewa/stock_management/blob/fd16b27c1f4898f0f5b0fc43297fa21870f0013f/apps_dir/product/views.py#L22
      - Tests:
        - [test for when a product with the required SKU exists](https://github.com/Telewa/stock_management/blob/master/apps_dir/product/tests/tests.py#L87)
        - [test for when a product with the required SKU DOES NOT exist](https://github.com/Telewa/stock_management/blob/master/apps_dir/product/tests/tests.py#L106)

   2. Consume stock from a product.
      - It does validate if the stock requested is available first, and then decrease it.
        - URL: https://github.com/Telewa/stock_management/blob/master/apps_dir/product/urls.py#L7
        - View: https://github.com/Telewa/stock_management/blob/fd16b27c1f4898f0f5b0fc43297fa21870f0013f/apps_dir/product/views.py#L41
        - Tests:
          - (Test for consuming a product progressively until there is no more left](https://github.com/Telewa/stock_management/blob/master/apps_dir/product/tests/tests.py#L126)
    
2. It has an API that allows bulk update of products from a CSV. 
   1. Foreach CSV line, the stock update could bepositive or negative. 
   2. If a product doesn't exist, it creates it.
    - URL: https://github.com/Telewa/stock_management/blob/master/apps_dir/product/urls.py#L5
    - View: https://github.com/Telewa/stock_management/blob/fd16b27c1f4898f0f5b0fc43297fa21870f0013f/apps_dir/product/views.py#L57
    - Tests: 
      - (Test for file upload and product creation)[https://github.com/Telewa/stock_management/blob/master/apps_dir/product/tests/tests.py#L36]
      - (Test for updating already extisting stock)[https://github.com/Telewa/stock_management/blob/master/apps_dir/product/tests/tests.py#L237]
