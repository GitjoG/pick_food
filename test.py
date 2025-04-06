import requests

def search_food_heat(keyword, page=1):
    """
    Search for food heat information using the mxnzp API
    
    Args:
        keyword (str): Food name to search for
        page (int): Page number for pagination
        
    Returns:
        dict: API response data
    """
    # API endpoint
    url = "https://www.mxnzp.com/api/food_heat/food/search"
    
    # You need to register for your own app_id and app_secret
    # Visit: https://mp.weixin.qq.com/s/UvKr0SG73_Py63ICUnLBPw
    params = {
        "keyword": keyword,
        "page": page,
        "app_id": "qtnozkkmgienmqav",  # Replace with your actual app_id
        "app_secret": "uMalUpkv60aTwXkj2cWoAqZYPTqC6yza"  # Replace with your actual app_secret
    }
    
    response = requests.get(url, params=params)
    return response.json()


def search_nutrition(food_id):
    url = "https://www.mxnzp.com/api/food_heat/food/details"
    params = {
        "foodId": food_id,
        "app_id": "qtnozkkmgienmqav",  # Replace with your actual app_id
        "app_secret": "uMalUpkv60aTwXkj2cWoAqZYPTqC6yza"  # Replace with your actual app_secret
    }
    response = requests.get(url, params=params)
    return response.json()

if __name__ == "__main__":
    
    
    # food_id = '26992e46910bbc2c'
    
    # result = search_nutrition(food_id)
    # print(result)
    # Example usage
    result = search_food_heat("烧鸭饭")  # Searching for "apple"
    print(result)
    
    food_id = result['data']['list'][0]['foodId']
    
    result = search_nutrition(food_id)
    print(result)
    
    
    # # If the API call is successful, you can process the data
    # if result.get("code") == 1:  # Assuming code 1 means success
    #     data = result.get("data")
    #     print(f"Found {len(data)} results")
    #     for item in data:
    #         print(item)
    # else:
    #     print(f"Error: {result.get('msg')}")
