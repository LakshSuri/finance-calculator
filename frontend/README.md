# Growth Laboratory — custom frontend preview

A local React/TypeScript interface calling the original calculator.py engine through a loopback-only Python API. This preview implements the combined growth workspace, yearly chart and CSV export. Other workspaces remain available through the unchanged Streamlit app. The development API is not intended for public deployment.

From the repository root, activate the existing Python environment and run `python growth_api.py`. In another terminal, run `cd frontend && npm install && npm run build && npm run dev`. Open http://127.0.0.1:5174. Run the full Python tests before committing. The production build still needs a production API and deployment configuration before hosting.
