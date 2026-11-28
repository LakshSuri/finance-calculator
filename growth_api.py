"""Loopback-only development API. Not a production HTTP server."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from urllib.parse import parse_qs, urlsplit
import calculator

LIMITS = {"principal": (0, 1e9), "monthly": (0, 1e9), "rate": (-99, 100), "years": (1, 50), "inflation": (-99, 100)}


def projection(query):
    if set(query) != set(LIMITS):
        raise ValueError("Supply principal, monthly, rate, years and inflation.")
    values = {}
    for name, (low, high) in LIMITS.items():
        if len(query[name]) != 1:
            raise ValueError(f"Supply one {name} value.")
        value = calculator.validate_number(query[name][0], name)
        if not low <= value <= high:
            raise ValueError(f"{name} must be between {low:g} and {high:g}.")
        values[name] = value
    years = calculator.validate_years(values["years"], minimum=1)
    return {"assumptions": values, "rows": [calculator.projection_breakdown(values["principal"], values["monthly"], values["rate"], year, values["inflation"]) for year in range(years+1)]}


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload, allow_nan=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlsplit(self.path)
        if path.path == "/api/health":
            self.send_json(200, {"status": "ok"})
            return
        if path.path != "/api/projection":
            self.send_json(404, {"error": "Unknown endpoint."})
            return
        try:
            data = projection(parse_qs(path.query, keep_blank_values=True, max_num_fields=5))
            self.send_json(200, data)
        except (ValueError, OverflowError) as exc:
            self.send_json(400, {"error": str(exc)})


if __name__ == "__main__":
    print("Local growth API: http://127.0.0.1:8765", flush=True)
    with ThreadingHTTPServer(("127.0.0.1", 8765), Handler) as server:
        server.serve_forever()
