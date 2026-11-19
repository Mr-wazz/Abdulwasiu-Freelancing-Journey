# Motion Team Portal: setup steps

You do these steps once. It takes about 30 minutes. Everything here is free.

You need two free accounts:
- **Supabase**: keeps the data, the logins and the screenshots.
- **Vercel**: puts the portal on the internet.

## Part 1: Supabase (the database)

1. Go to supabase.com and sign up with your Google or GitHub account.
2. Click **New project**. Name it `motion`. Choose a strong database password and save it somewhere safe. For region, choose the one closest to Nigeria that is offered (for example West EU or Cape Town). Click **Create new project** and wait about 2 minutes.
3. In the left menu click **SQL Editor**, then **New query**.
4. Open the file `supabase/schema.sql` from this folder. Copy all of it, paste it into the editor, and click **Run**. You should see "Success. No rows returned".
5. In the left menu click **Authentication**, then **Sign In / Providers**, then **Email**. Turn **Confirm email** off and save. Reason: your members join with a private invite link from you, so the extra email step only slows them down.
6. In the left menu click **Project Settings**, then **API** (or **Data API**). Copy two values and keep them for Part 2:
   - **Project URL** (looks like `https://abcd1234.supabase.co`)
   - **anon public** key (a long text). This key is safe to put in the app. Never share the `service_role` key.

## Part 2: Vercel (the website)

1. Go to vercel.com and sign up with your GitHub account.
2. Click **Add New**, then **Project**, and import the `Abdulwasiu-Freelancing-Journey` repository.
3. Set **Root Directory** to `projects/motion/02-work/portal`. Vercel should detect **Vite** by itself.
4. Open **Environment Variables** and add these two:
   - `VITE_SUPABASE_URL` = your Project URL
   - `VITE_SUPABASE_ANON_KEY` = your anon public key
5. Click **Deploy**. After a minute you get a link like `https://motion-portal.vercel.app`. That is your portal.
6. Go back to Supabase: **Authentication**, then **URL Configuration**. Put your Vercel link in **Site URL** and save. This makes the "forgot password" emails come back to your portal.

## Part 3: Make yourself the admin

Do this right away, before you share the link with anyone. **The first account created becomes the admin.**

1. Open your portal link. Click **Join the team**.
2. Enter your name, email and a password. Leave the invite code empty. Click **Create my account**.
3. You should land on the **Team dashboard**. If you see it, you are the admin.

## Part 4: Load your team

1. **More, then Team setup**: set the value of one point (BV per PV in Naira). To get it, take a product from the NeoLife price list and divide its BV by its PV.
2. **More, then Products**: click **Paste a price list**. Put your price list in Excel or Google Sheets with the columns Name, Code, PV, BV, Distributor price, Retail price. Copy the rows and paste them.
3. **Team, then Add member**: add each of your 9 members. Choose their sponsor. Start with the people you sponsored yourself, then the people they sponsored.
4. Open each member, click **Create invite link**, then **Copy WhatsApp message**, and send it to them. They click the link, choose a password, and they are in.

## Good to know

- **Free plan sleep**: a free Supabase project pauses if nobody uses it for 7 days. With a team using it daily this will not happen. If it does, open Supabase and click **Restore**.
- **Forgot password**: members click "Forgot password" on the sign in page. The free Supabase plan sends only a few emails per hour. That is fine for a team of 30.
- **Someone joined without an invite link**: they wait in your **Inbox**. Open them, choose their sponsor, and approve. Or decline.
- **A member leaves**: open the member and click **Switch off**. Their records stay, but they can no longer sign in to the portal's data.
- **Your own domain**: in Vercel, open the project, then **Domains**. Add a domain like `motionteam.com.ng`. Then update the Site URL in Supabase.

## For a developer

```
npm install
cp .env.example .env    # then fill in the two Supabase values
npm run dev             # local preview. With no .env it runs on sample data
npm test                # bonus maths, goal breakdown, tree, price list paste
npm run build           # live build into dist/
npm run build:demo      # one self contained demo file into dist-demo/
tests/sql/run.sh        # tests schema.sql and every privacy rule on a local Postgres
NODE_PATH=$(npm root -g) node scripts/e2e.mjs   # click through test of the demo (needs Playwright)
```
