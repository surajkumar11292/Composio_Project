from dataclasses import dataclass
from typing import List

@dataclass
class AppEntry:
    id: str
    name: str
    category: str
    homepage: str
    docs_hint: str
    priority: int

APPS: List[AppEntry] = [
    # 1. CRM & Sales
    AppEntry("salesforce", "Salesforce", "CRM & Sales", "https://www.salesforce.com", "developer API REST OAuth", 1),
    AppEntry("hubspot", "HubSpot", "CRM & Sales", "https://www.hubspot.com", "developers API authentication", 1),
    AppEntry("pipedrive", "Pipedrive", "CRM & Sales", "https://www.pipedrive.com", "developers API token", 1),
    AppEntry("attio", "Attio", "CRM & Sales", "https://attio.com", "developers API OAuth", 2),
    AppEntry("zoho_crm", "Zoho CRM", "CRM & Sales", "https://www.zoho.com/crm/", "developer API OAuth2", 2),
    AppEntry("close", "Close", "CRM & Sales", "https://close.com", "developers API key", 2),
    AppEntry("freshsales", "Freshsales", "CRM & Sales", "https://www.freshworks.com/crm/sales/", "developers API token", 2),
    AppEntry("apollo", "Apollo.io", "CRM & Sales", "https://www.apollo.io", "developer API key", 3),
    AppEntry("copper", "Copper", "CRM & Sales", "https://www.copper.com", "developer API REST", 3),
    AppEntry("streak", "Streak", "CRM & Sales", "https://www.streak.com", "developer API key", 3),

    # 2. Support & CS
    AppEntry("zendesk", "Zendesk", "Support & CS", "https://www.zendesk.com", "developer API OAuth", 1),
    AppEntry("intercom", "Intercom", "Support & CS", "https://www.intercom.com", "developers API token", 1),
    AppEntry("freshdesk", "Freshdesk", "Support & CS", "https://freshdesk.com", "developers API key", 1),
    AppEntry("helpscout", "Help Scout", "Support & CS", "https://www.helpscout.com", "developers API OAuth2", 2),
    AppEntry("gorgias", "Gorgias", "Support & CS", "https://www.gorgias.com", "developers API REST", 2),
    AppEntry("liveagent", "LiveAgent", "Support & CS", "https://www.liveagent.com", "developers API key", 2),
    AppEntry("gladly", "Gladly", "Support & CS", "https://www.gladly.com", "developer API REST", 3),
    AppEntry("kustomer", "Kustomer", "Support & CS", "https://www.kustomer.com", "developer API REST", 3),
    AppEntry("front", "Front", "Support & CS", "https://front.com", "developers API token", 2),
    AppEntry("tidio", "Tidio", "Support & CS", "https://www.tidio.com", "developer API OAuth", 3),

    # 3. Comms & Messaging
    AppEntry("slack", "Slack", "Comms & Messaging", "https://slack.com", "api docs OAuth2", 1),
    AppEntry("twilio", "Twilio", "Comms & Messaging", "https://www.twilio.com", "docs API key REST", 1),
    AppEntry("discord", "Discord", "Comms & Messaging", "https://discord.com", "developer portal API OAuth2", 1),
    AppEntry("telegram", "Telegram", "Comms & Messaging", "https://telegram.org", "bot API token", 1),
    AppEntry("whatsapp_business", "WhatsApp Business", "Comms & Messaging", "https://business.whatsapp.com", "cloud API token", 2),
    AppEntry("sendbird", "Sendbird", "Comms & Messaging", "https://sendbird.com", "docs API token", 2),
    AppEntry("vonage", "Vonage", "Comms & Messaging", "https://www.vonage.com", "developer API key", 2),
    AppEntry("bandwidth", "Bandwidth", "Comms & Messaging", "https://www.bandwidth.com", "developer API REST", 3),
    AppEntry("plivo", "Plivo", "Comms & Messaging", "https://www.plivo.com", "docs API auth id", 3),
    AppEntry("ringcentral", "RingCentral", "Comms & Messaging", "https://www.ringcentral.com", "developers API OAuth", 3),

    # 4. Marketing & Social
    AppEntry("mailchimp", "Mailchimp", "Marketing & Social", "https://mailchimp.com", "developer API key OAuth2", 1),
    AppEntry("klaviyo", "Klaviyo", "Marketing & Social", "https://www.klaviyo.com", "developers API key", 1),
    AppEntry("sendgrid", "SendGrid", "Marketing & Social", "https://sendgrid.com", "docs API key", 1),
    AppEntry("brevo", "Brevo", "Marketing & Social", "https://www.brevo.com", "developers API key", 2),
    AppEntry("hubspot_marketing", "HubSpot Marketing", "Marketing & Social", "https://www.hubspot.com/products/marketing", "developers API OAuth", 2),
    AppEntry("pinterest", "Pinterest", "Marketing & Social", "https://www.pinterest.com", "developers API OAuth2", 2),
    AppEntry("threads", "Threads API", "Marketing & Social", "https://developers.facebook.com/docs/threads", "API Graph OAuth", 2),
    AppEntry("beehiiv", "Beehiiv", "Marketing & Social", "https://www.beehiiv.com", "developers API key", 2),
    AppEntry("activecampaign", "ActiveCampaign", "Marketing & Social", "https://www.activecampaign.com", "developers API key", 3),
    AppEntry("postmark", "Postmark", "Marketing & Social", "https://postmarkapp.com", "developer API token", 3),

    # 5. Ecommerce
    AppEntry("shopify", "Shopify", "Ecommerce", "https://www.shopify.com", "developers API OAuth GraphQL REST", 1),
    AppEntry("woocommerce", "WooCommerce", "Ecommerce", "https://woocommerce.com", "docs REST API key", 1),
    AppEntry("bigcommerce", "BigCommerce", "Ecommerce", "https://www.bigcommerce.com", "developer API token", 1),
    AppEntry("magento", "Magento", "Ecommerce", "https://business.adobe.com/products/magento/magento-commerce.html", "devdocs API REST", 2),
    AppEntry("woopayments", "WooPayments", "Ecommerce", "https://woocommerce.com/payments/", "docs REST API", 2),
    AppEntry("printify", "Printify", "Ecommerce", "https://printify.com", "developers API key", 2),
    AppEntry("printful", "Printful", "Ecommerce", "https://www.printful.com", "developers API OAuth", 2),
    AppEntry("shippo", "Shippo", "Ecommerce", "https://goshippo.com", "docs API token", 3),
    AppEntry("easypost", "EasyPost", "Ecommerce", "https://www.easypost.com", "docs API key", 3),
    AppEntry("ecwid", "Ecwid", "Ecommerce", "https://www.ecwid.com", "developers API token OAuth", 3),

    # 6. Research & Enrichment
    AppEntry("ahrefs", "Ahrefs", "Research & Enrichment", "https://ahrefs.com", "docs API token", 1),
    AppEntry("apify", "Apify", "Research & Enrichment", "https://apify.com", "docs API token", 1),
    AppEntry("firecrawl", "Firecrawl", "Research & Enrichment", "https://www.firecrawl.dev", "docs API key", 1),
    AppEntry("clay", "Clay", "Research & Enrichment", "https://www.clay.com", "developers API key", 2),
    AppEntry("bright_data", "Bright Data", "Research & Enrichment", "https://brightdata.com", "docs API token", 2),
    AppEntry("hunter_io", "Hunter.io", "Research & Enrichment", "https://hunter.io", "docs API key", 2),
    AppEntry("clearbit", "Clearbit", "Research & Enrichment", "https://clearbit.com", "docs API key", 2),
    AppEntry("phantombuster", "PhantomBuster", "Research & Enrichment", "https://phantombuster.com", "developers API key", 3),
    AppEntry("exa_ai", "Exa.ai", "Research & Enrichment", "https://exa.ai", "docs API key", 3),
    AppEntry("diffbot", "Diffbot", "Research & Enrichment", "https://www.diffbot.com", "docs API token", 3),

    # 7. Dev, Infra & Data
    AppEntry("github", "GitHub", "Dev, Infra & Data", "https://github.com", "docs API REST GraphQL PAT", 1),
    AppEntry("vercel", "Vercel", "Dev, Infra & Data", "https://vercel.com", "docs API token REST", 1),
    AppEntry("netlify", "Netlify", "Dev, Infra & Data", "https://www.netlify.com", "docs API OAuth token", 1),
    AppEntry("cloudflare", "Cloudflare", "Dev, Infra & Data", "https://www.cloudflare.com", "developers API token", 1),
    AppEntry("supabase", "Supabase", "Dev, Infra & Data", "https://supabase.com", "docs API key JWT", 2),
    AppEntry("railway", "Railway", "Dev, Infra & Data", "https://railway.app", "docs API GraphQL token", 2),
    AppEntry("render", "Render", "Dev, Infra & Data", "https://render.com", "docs API key REST", 2),
    AppEntry("planetscale", "PlanetScale", "Dev, Infra & Data", "https://planetscale.com", "docs API token", 3),
    AppEntry("neon", "Neon", "Dev, Infra & Data", "https://neon.tech", "docs API key REST", 3),
    AppEntry("fly_io", "Fly.io", "Dev, Infra & Data", "https://fly.io", "docs API token GraphQL", 3),

    # 8. Productivity & PM
    AppEntry("linear", "Linear", "Productivity & PM", "https://linear.app", "docs API GraphQL OAuth", 1),
    AppEntry("jira", "Jira", "Productivity & PM", "https://www.atlassian.com/software/jira", "developer API REST OAuth", 1),
    AppEntry("asana", "Asana", "Productivity & PM", "https://asana.com", "developers API PAT OAuth", 1),
    AppEntry("monday", "Monday.com", "Productivity & PM", "https://monday.com", "developers API GraphQL token", 2),
    AppEntry("clickup", "ClickUp", "Productivity & PM", "https://clickup.com", "docs API token OAuth", 2),
    AppEntry("notion", "Notion", "Productivity & PM", "https://www.notion.so", "developers API integration token", 2),
    AppEntry("todoist", "Todoist", "Productivity & PM", "https://todoist.com", "developer API REST token", 2),
    AppEntry("height", "Height", "Productivity & PM", "https://height.app", "docs API token REST", 3),
    AppEntry("basecamp", "Basecamp", "Productivity & PM", "https://basecamp.com", "github API OAuth", 3),
    AppEntry("plane", "Plane", "Productivity & PM", "https://plane.so", "docs API token", 3),

    # 9. Finance & Fintech
    AppEntry("stripe", "Stripe", "Finance & Fintech", "https://stripe.com", "docs API keys REST", 1),
    AppEntry("plaid", "Plaid", "Finance & Fintech", "https://plaid.com", "docs API keys", 1),
    AppEntry("binance", "Binance", "Finance & Fintech", "https://www.binance.com", "docs API key secret", 1),
    AppEntry("braintree", "Braintree", "Finance & Fintech", "https://www.braintreepayments.com", "developers API GraphQL keys", 2),
    AppEntry("razorpay", "Razorpay", "Finance & Fintech", "https://razorpay.com", "docs API keys basic", 2),
    AppEntry("wise", "Wise", "Finance & Fintech", "https://wise.com", "docs API token RSA", 2),
    AppEntry("coinbase", "Coinbase", "Finance & Fintech", "https://www.coinbase.com", "docs API keys REST", 3),
    AppEntry("dwolla", "Dwolla", "Finance & Fintech", "https://www.dwolla.com", "docs API OAuth", 3),
    AppEntry("finix", "Finix", "Finance & Fintech", "https://www.finix.com", "docs API basic auth", 3),
    AppEntry("adyen", "Adyen", "Finance & Fintech", "https://www.adyen.com", "docs API key basic", 3),

    # 10. AI, Video & Audio
    AppEntry("fathom", "Fathom", "AI, Video & Audio", "https://fathom.video", "docs API token", 1),
    AppEntry("reducto", "Reducto", "AI, Video & Audio", "https://reducto.ai", "docs API key", 1),
    AppEntry("grain", "Grain", "AI, Video & Audio", "https://grain.com", "docs API developer", 1),
    AppEntry("fireflies_ai", "Fireflies.ai", "AI, Video & Audio", "https://fireflies.ai", "docs API GraphQL token", 2),
    AppEntry("otter_ai", "Otter.ai", "AI, Video & Audio", "https://otter.ai", "developer API access", 2),
    AppEntry("assemblyai", "AssemblyAI", "AI, Video & Audio", "https://www.assemblyai.com", "docs API token REST", 2),
    AppEntry("deepgram", "Deepgram", "AI, Video & Audio", "https://deepgram.com", "docs API key", 2),
    AppEntry("elevenlabs", "ElevenLabs", "AI, Video & Audio", "https://elevenlabs.io", "docs API key REST", 3),
    AppEntry("runway", "Runway", "AI, Video & Audio", "https://runwayml.com", "docs API developer", 3),
    AppEntry("synthesia", "Synthesia", "AI, Video & Audio", "https://www.synthesia.io", "docs API key", 3),
]
