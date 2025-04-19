import { Router } from 'express'
import { readdirSync } from 'fs'
import { join } from 'path'
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export default (app) => {
  const router = Router()
  app.use('/api', router)
  readdirSync(join(__dirname, '../routes')).map(async file => {
      (await import(`../routes/${file}`)).default(router)
  })
}
