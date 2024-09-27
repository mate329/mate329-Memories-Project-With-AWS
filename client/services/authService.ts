export async function processAuthRequest(loginRequest: object, endpoint: String): Promise<void> {
    const res = await fetch(
      `${process.env.NEXT_PUBLIC_AUTH_ROUTE}/Prod/${endpoint}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(loginRequest),
      }
    );
  
    if (!res.ok) {
      throw new Error("Failed to create post");
    }
}