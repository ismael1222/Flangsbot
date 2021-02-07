CREATE TABLE IF NOt EXISTS exp (
    UserID integer PRIMARY key,
    XP integer DEFAULT 0,
    Level integer DEFAULT 0,
    XPLock text DEFAULT CURRENT_TIMESTAMP
);