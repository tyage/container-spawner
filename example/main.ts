import { serve, ServerRequest } from "https://deno.land/std@0.106.0/http/server.ts";
import { decode } from "https://deno.land/std@0.106.0/encoding/base64.ts";

// simple basic auth implementation
// we can use CS_USERNAME and CS_PASSWORD which come from Container Spawner
const basicAuthUser = Deno.env.get('CS_USERNAME');
const basicAuthPassword = Deno.env.get('CS_PASSWORD');
const verifyBasicAuth = (req: ServerRequest) => {
  const authorization = req.headers.get('authorization');
  if (!authorization) {
    return false;
  }
  const payload = authorization.split(' ')[1];
  const authText = new TextDecoder().decode(decode(payload));
  const [user, password] = authText.split(':');
  return (user === basicAuthUser && password === basicAuthPassword);
};

// start app
const PORT = 1993;
const s = serve(`0.0.0.0:${PORT}`);
console.log(`Server started on port ${PORT}`);

for await (const req of s) {
  if (verifyBasicAuth(req)) {
    // verified!
    const body = new TextEncoder().encode("Hello World\n");
    req.respond({ body });
  } else {
    // not verified
    const body = new TextEncoder().encode("Not allowed\n");
    const headers = new Headers();
    headers.set('www-authenticate', 'Basic realm="example"');
    req.respond({ status: 401, body, headers });
  }
}
