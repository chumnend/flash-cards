CREATE TABLE decks (
    id UUID NOT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    publish_status VARCHAR(20) DEFAULT 'private',
    owner_id UUID NOT NULL,
    rating DECIMAL(2,1) DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
    CHECK (publish_status IN ('private', 'public')),
    CHECK (rating >= 0.0 AND rating <= 5.0)
);
