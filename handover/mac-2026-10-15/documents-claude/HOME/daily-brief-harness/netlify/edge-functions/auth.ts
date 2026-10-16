// Basic-auth gate for the brief. Free-tier substitute for Netlify's paid
// password protection. Set BRIEF_USER / BRIEF_PASS in Netlify env vars.
export default async (request: Request, context: any) => {
  const auth = request.headers.get("authorization") || "";
  const expected = "Basic " + btoa(`${Deno.env.get("BRIEF_USER")}:${Deno.env.get("BRIEF_PASS")}`);
  if (auth === expected) return context.next();
  return new Response("Auth required", {
    status: 401,
    headers: { "WWW-Authenticate": 'Basic realm="daily-brief"', "X-Robots-Tag": "noindex" },
  });
};
