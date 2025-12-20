import { NextRequest, NextResponse } from "next/server";

export function proxy(request: NextRequest) {
  // Extract subdomain from the hostname
  const hostname = request.headers.get("host") || request.nextUrl.hostname;
  const subdomain = extractSubdomain(hostname);

  const requestHeaders = new Headers(request.headers);
  if (subdomain) {
    requestHeaders.set("x-tenant-id", subdomain);
  }

  const response = NextResponse.next({
    request: {
      headers: requestHeaders,
    },
  });

  // Optionally, you can also set it as a response header
  if (subdomain) {
    response.headers.set("x-subdomain", subdomain);
  }

  return response;
}


function extractSubdomain(hostname: string): string | null {
  const hostWithoutPort = hostname.split(":")[0];

  const parts = hostWithoutPort.split(".");

  if (parts.length >= 3 && !isLocalhost(hostWithoutPort) && !isIPAddress(hostWithoutPort)) {
    return parts[0];
  }

  // For localhost or IP addresses, return minimal for development
  return "minimal";
}

function isLocalhost(hostname: string): boolean {
  return hostname === "localhost" || hostname.startsWith("127.0.0.1") || hostname.startsWith("0.0.0.0");
}

function isIPAddress(hostname: string): boolean {
  // Simple check for IPv4
  const ipv4Regex = /^(\d{1,3}\.){3}\d{1,3}$/;
  return ipv4Regex.test(hostname);
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};