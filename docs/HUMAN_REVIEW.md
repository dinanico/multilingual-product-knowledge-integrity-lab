# Human Review

Critical factual drift or a missing critical claim creates a `PENDING_REVIEW` task. A reviewer may approve, reject, or require correction. Correction creates a new target version derived from the faulty version; the historical finding remains intact. The new candidate must pass QA before `APPROVED_FOR_PUBLICATION`.

Human-in-the-loop does not mean people translate everything. It means a person intervenes where risk or uncertainty justifies it.
