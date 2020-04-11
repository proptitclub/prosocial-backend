import mysql from 'mysql2';

export const connection = mysql.createConnection({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  port: '3306',
  database: process.env.DB_NAME,
});