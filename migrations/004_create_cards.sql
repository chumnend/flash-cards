CREATE TABLE cards (
    id UUID NOT NULL UNIQUE,
    front_text TEXT NOT NULL,
    back_text TEXT NOT NULL,
    difficulty VARCHAR(20) DEFAULT 'easy',
    times_reviewed INTEGER DEFAULT 0,
    success_rate DECIMAL(5,2) DEFAULT 0.00,
    deck_id UUID NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (deck_id) REFERENCES decks(id) ON DELETE CASCADE,
    CHECK (difficulty IN ('easy', 'medium', 'hard')),
    CHECK (success_rate >= 0.00 AND success_rate <= 100.00)
);
