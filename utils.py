import os, asyncpg, typing as t

from config import *

def get_database_url(
        DEFAULT_DB_HOST: str = "localhost",
        DEFAULT_DB_PORT: str = "5432",
        DEFAULT_DB_NAME: str = "filestorage",
        DEFAULT_DB_USER: str = "fileStorageuser",
        DEFAULT_DB_PASSWORD: str = "fileStoragePassword"
    ) -> str:
    """
    Returns the database URL based on the provided or default values.

    Args:
        DEFAULT_DB_HOST: The default database host.
        DEFAULT_DB_PORT: The default database port.
        DEFAULT_DB_NAME: The default database name.
        DEFAULT_DB_USER: The default database user.
        DEFAULT_DB_PASSWORD: The default database password.

    Returns: The database URL.
    """
    db_host = os.environ.get("DB_HOST", DEFAULT_DB_HOST)
    db_port = os.environ.get("DB_PORT", DEFAULT_DB_PORT)
    db_name = os.environ.get("DB_NAME", DEFAULT_DB_NAME)
    db_user = os.environ.get("DB_USER", DEFAULT_DB_USER)
    db_password = os.environ.get("DB_PASSWORD", DEFAULT_DB_PASSWORD)

    return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


async def prepare_server():
    """
    Prepares the server by creating necessary database tables and directories.
    """
    DATA_FOLDER.mkdir(parents=True, exist_ok=True)

    DATABASE_URL = get_database_url()
    
    connection = await asyncpg.connect(DATABASE_URL)
    try:        
        await connection.execute(
            """
            CREATE TABLE IF NOT EXISTS files (
                id SERIAL PRIMARY KEY,
                file_name TEXT,
                file_size INT,
                dir_name TEXT REFERENCES directories(dir_name),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        
        await connection.execute(
            """
            ALTER TABLE files DROP CONSTRAINT IF EXISTS files_unique_constraint;
            ALTER TABLE files ADD CONSTRAINT files_unique_constraint UNIQUE (file_name, dir_name);
            """
        )
        
        await connection.execute(
            """
            CREATE TABLE IF NOT EXISTS directories (
                id SERIAL PRIMARY KEY,
                dir_name TEXT UNIQUE
            )
            """
        )

        await connection.execute(
            """
            INSERT INTO directories (dir_name) VALUES ($1) ON CONFLICT DO NOTHING
            """,
            "."
        )
    finally:
        await connection.close()


async def save_file_to_db(connection: asyncpg.Connection, dir_name: str, filename: str, filesize: int) -> int:
    """
    Saves a file to the database.

    Args:
        connection: The database connection object.
        dir_name (str): The name of the directory.
        filename (str): The name of the file.
        filesize (int): The size of the file in bytes.

    Returns:
        int: The ID of the saved file.
    """
    await connection.execute("INSERT INTO directories (dir_name) VALUES ($1) ON CONFLICT DO NOTHING", dir_name)
    query = """
        INSERT INTO files (file_name, dir_name, file_size) 
        VALUES ($1, $2, $3)
        ON CONFLICT (file_name, dir_name) DO UPDATE
        SET updated_at = CURRENT_TIMESTAMP, file_size = $3
        RETURNING id
    """
    
    file_id = await connection.fetchval(query, filename, dir_name, filesize)
    return file_id


async def get_file_info_by_id(connection: asyncpg.Connection, file_id: int) -> t.Optional[asyncpg.Record]:
    """
    Retrieves file information by its ID from the database.

    Args:
        connection (asyncpg.Connection): The database connection.
        file_id (int): The ID of the file to retrieve information for.

    Returns:
        dict: A dictionary containing the file information, including filename, directory name, file size, and last updated time.

    """
    query = "SELECT file_name, dir_name, file_size, updated_at FROM files WHERE id = $1"
    return await connection.fetchrow(query, file_id)


async def get_top_files(connection: asyncpg.Connection, dir_name: str = None) -> t.List[asyncpg.Record]:
    """
    Retrieves the top files based on file size from the database.

    Args:
        connection (asyncpg.Connection): The database connection object.
        dir_name (str, optional): The directory name to filter the files. Defaults to None.

    Returns:
        List[asyncpg.Record]: A list of database records containing file_name, file_size, and last updated time.
    """
    query = f"""
        SELECT file_name, file_size, updated_at
        FROM files
        {"WHERE dir_name = $1" if dir_name else ""}
        ORDER BY file_size DESC
        LIMIT 10
    """
    return await connection.fetch(query, dir_name) if dir_name else await connection.fetch(query)