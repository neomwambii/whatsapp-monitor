import azure.functions as func
import logging
import json
from datetime import datetime
from email_notifier import EmailNotifier
import config

app = func.FunctionApp()

@app.timer_trigger(schedule="0 0 14 * * 2", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
def tuesday_monitoring(myTimer: func.TimerRequest) -> None:
    """Azure Function triggered every Tuesday at 2:00 PM"""
    utc_timestamp = datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()
    
    if myTimer.past_due:
        logging.info('The timer is past due!')
    
    logging.info('Tuesday monitoring triggered at %s', utc_timestamp)
    
    try:
        # For now, just send a test notification
        # In production, this would run the WhatsApp monitoring
        notifier = EmailNotifier()
        notifier.send_approval_notification(
            "DEMO: Good news: We have approval from SBIB and Liberty for tonights deploy",
            "Paris group 2"
        )
        logging.info('Tuesday monitoring completed successfully')
    except Exception as e:
        logging.error(f'Error in Tuesday monitoring: {str(e)}')
        notifier = EmailNotifier()
        notifier.send_error_notification(str(e))

@app.function_name(name="ManualCheck")
@app.route(route="manual-check", methods=["POST"])
def manual_check(req: func.HttpRequest) -> func.HttpResponse:
    """Manual trigger for monitoring (for flexible scheduling)"""
    logging.info('Manual check triggered')
    
    try:
        notifier = EmailNotifier()
        notifier.send_approval_notification(
            "MANUAL TRIGGER: Good news: We have approval from SBIB and Liberty for tonights deploy",
            "Paris group 2"
        )
        
        return func.HttpResponse(
            json.dumps({"status": "success", "message": "Manual check completed"}),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f'Error in manual check: {str(e)}')
        return func.HttpResponse(
            json.dumps({"status": "error", "message": str(e)}),
            status_code=500,
            mimetype="application/json"
        )

@app.function_name(name="HealthCheck")
@app.route(route="health", methods=["GET"])
def health_check(req: func.HttpRequest) -> func.HttpResponse:
    """Health check endpoint"""
    return func.HttpResponse(
        json.dumps({"status": "healthy", "timestamp": datetime.utcnow().isoformat()}),
        status_code=200,
        mimetype="application/json"
    )
