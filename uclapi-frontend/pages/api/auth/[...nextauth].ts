import NextAuth from "next-auth";

const makeTokenRequest = async (context) =>
  fetch(
    `${context.provider.token.url}?code=${context.params.code}&client_id=${context.client.client_id}&client_secret=${context.client.client_secret}`
  ).then((res) => res.json());

const makeUserInfoRequest = async (context) =>
  fetch(
    `${context.provider.userinfo.url}?client_secret=${context.client.client_secret}&token=${context.tokens.access_token}`
  ).then((res) => res.json());

export const authOptions = {
  providers: [
    {
      id: "uclapi",
      name: "UCL API",
      type: "oauth",
      authorization: `${process.env.UCLAPI_DOMAIN}/oauth/authorise`,
      token: {
        url: `${process.env.UCLAPI_DOMAIN}/oauth/token`,
        async request(context) {
          const tokens = await makeTokenRequest(context);
          return { tokens };
        },
      },
      userinfo: {
        url: `${process.env.UCLAPI_DOMAIN}/oauth/user/data`,
        async request(context) {
          return await makeUserInfoRequest(context);
        },
      },
      clientId: process.env.UCL_API_CLIENT_ID,
      clientSecret: process.env.UCL_API_CLIENT_SECRET,
      profile(profile) {
        return {
          id: profile.cn,
          name: profile.full_name,
          email: profile.email,
          upi: profile.upi,
          image: "",
        };
      },
    },
  ],
  secret: process.env.NEXTAUTH_SECRET,
  callbacks: {
    session: async ({ session, token }) => {
      // Called on every request to get the session
      // Adds the isAdmin flag to the session.user object
      if (token?.sub != null && session?.user != null) {
        session.user.uclGroups = token.uclGroups;
      }
      return session;
    },
    jwt: async ({ token, profile }) => {
      // Called when a JWT is created (on sign in) or updated
      if (profile) token.uclGroups = profile.ucl_groups;
      return token;
    },
    signIn: async ({ profile }) => {
      return profile.user_types.some((x) =>
        ["Casual", "Honorary", "P/G", "Staff", "U/G"].includes(x)
      );
    },
  },
  session: {
    maxAge: 24 * 60 * 60, // One day idle session expiry
  },
};

/**
 * NextAuth.js configuration. See https://next-auth.js.org/configuration/initialization for details.
 * We use a custom OAuth provider to point NextAuth.js towards UCL API's OAuth system.
 * We also use NextAuth.js callbacks to ensure only Engineering users can login, and to grant admin privileges.
*/
export default NextAuth(authOptions);
