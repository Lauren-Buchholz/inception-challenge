# Inception Health Technical Challenge

## Assignment

* Using the tools and language of your choice, write code that deploys the application provided in `app/` using a single command.
* The single command from the user can (and likely will) call a longer shell script, or other configuration management code.
* The script should make the backend service available via https over the public internet.
* The script should output the address of the `backend` api.
* The script should cause the checkin event handler to be triggered regularly by an automated process.
* Your credentials are attached. You have admin access to the account. Please use region `us-east-1`.
* We ask that you not use ec2 directly for your solution. However, something like a fargate cluster in which ec2 instances are managed by aws is okay.
* You should not need to make changes to the existing application code. 

## Evaluation Criteria

* Please don't take more than 3 hours total. If you find yourself running over, write down what you didn't get to so we can discuss it in the review.
* Timekeeping is up to you and we expect your finished response in a reasonable amount of time.
* Source control is expected as well as documentation that should explain how you approached the challenge, what assumptions you've made, and reasoning behind the choices in your approach.
* You are being evaluated based on:
  * Quality of your code and configuration
  * Clarity of your written communication and documentation
  * Communicating how your code works in our review session.
  * Communicating how the app runs in our review session.
  * Project presentation.
