const { execSync } = require('child_process');
const { Client } = require('pg');

const dbConfig = {
    user: 'user',
    password: 'password',
    host: 'localhost',
    port: 5432,
    database: 'ecommerce_db'
};

describe('ETL Pipeline Integration Tests', () => {
    let client;

    beforeAll(async () => {
        client = new Client(dbConfig);
        await client.connect();
        // Clear tables before test
        await client.query('TRUNCATE fact_transactions, dim_customers, dim_products CASCADE');
    });

    afterAll(async () => {
        await client.end();
    });

    test('Python ETL should populate PostgreSQL correctly', async () => {
        // 1. Execute the Python ETL script
        execSync('python etl.py');

        // 2. Test Data Transformation (Did it drop FAILED logs?)
        const factRes = await client.query('SELECT COUNT(*) FROM fact_transactions');
        expect(parseInt(factRes.rows[0].count)).toBe(4); // 5 rows total, 1 was FAILED

        // 3. Test Data Cleaning (Did it fix "John doe" to "John Doe"?)
        const userRes = await client.query('SELECT user_name FROM dim_customers WHERE user_id = 1');
        expect(userRes.rows[0].user_name).toBe('John Doe');

        // 4. Test Missing Value Handling (Did Alice's NULL price become 0?)
        const priceRes = await client.query('SELECT revenue FROM fact_transactions WHERE user_id = 3');
        expect(parseFloat(priceRes.rows[0].revenue)).toBe(0);
    });
});