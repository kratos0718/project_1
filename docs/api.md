# API Documentation

Base URL: `http://localhost:8000/api`

## Health

`GET /health`

Returns service status.

## Submit Complaint

`POST /complaints`

```json
{
  "text": "Sewage water has been overflowing near the school gate for three days and children are walking through it.",
  "locality": "Ward 12",
  "category": "sanitation",
  "metadata": {
    "source": "web",
    "landmark": "Government School"
  }
}
```

Response includes cleaned text, severity score, escalation priority, retrieved citations, duplicate IDs, and agent reasoning trace.

## List Complaints

`GET /complaints?limit=25`

Returns most recent complaints.

## Analytics

`GET /analytics`

Returns total complaints, open complaints, severity distribution, locality counts, and trend points.

