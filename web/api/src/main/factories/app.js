import express from 'express'
import setupRoutes from './routes.js'

export const makeApp = async () => {
  const app = express()
  setupRoutes(app)
  return app
}
