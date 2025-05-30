import * as path from "path";
import * as dotenv from 'dotenv';

dotenv.config({ path: path.resolve(__dirname, "../.env") });

import { AppDataSource } from './data-source';
import app from './app';


const PORT = process.env.PORT || 3000;


console.log(">> HOST VAR:", process.env.POSTGRES_HOST);
AppDataSource.initialize().then(() => {
  app.listen(PORT, () => {
    console.log(`Server started on port ${PORT}`);
  });
}).catch(error => {
  console.error('Failed to connect to database', error);
});