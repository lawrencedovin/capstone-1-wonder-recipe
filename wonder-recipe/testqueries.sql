SELECT r.recipe_name, c.cuisine_name
    FROM recipes r
    JOIN cuisines c
        ON r.cuisine_id = c.id;