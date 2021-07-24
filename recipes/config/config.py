import yaml

with open('../config/config.yaml') as file:
    config = yaml.safe_load(file)

# Headers for recipes' table
RECIPES_HEADERS = ('Recipe ID', 'User ID', 'Recipe Name', 'Creation Date',
                   'Recipe Description', 'Likes', 'Recipe Status', 'Tags')
RECIPE_KEYS = ((0, 'id'), (0, 'user_id'), (0, 'recipe_name'), (0, 'create_date'),
               (0, 'recipe_description'), (0, 'likes'), (0, 'status'), (1, 'list'))
RECIPE_KEYS_FILTER = ('id', 'user_id', 'recipe_name', 'create_date', 'recipe_description', 'likes', 'status')
RECIPE_KEYS_NOT_SINGLE = ((0, 'id'), (0, 'user_id'), (0, 'recipe_name'), (0, 'create_date'),
                          (0, 'recipe_description'), (0, 'likes'), (0, 'status'))
USERS_AND_QUANTITY_HEADERS = ('ID', 'Nickname', 'Status', 'Online', 'Quantity of recipes')