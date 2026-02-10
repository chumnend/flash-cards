CREATE TABLE deck_categories (
    deck_id UUID NOT NULL,
    category_id UUID NOT NULL,
    PRIMARY KEY (deck_id, category_id),
    FOREIGN KEY (deck_id) REFERENCES decks(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);
