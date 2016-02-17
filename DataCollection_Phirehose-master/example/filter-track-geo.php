<?php
require_once('../lib/Phirehose.php');
require_once('../lib/OauthPhirehose.php');

/**
 * Example of using Phirehose to display a live filtered stream using geo locations
 */
class FilterTrackConsumer extends OauthPhirehose
{
  /**
   * Enqueue each status
   *
   * @param string $status
   */
  public function enqueueStatus($status)
  {
    /*
     * In this simple example, we will just display to STDOUT rather than enqueue.
     * NOTE: You should NOT be processing tweets at this point in a real application, instead they should be being
     *       enqueued and processed asyncronously from the collection process.
     */
    $data = json_decode($status, true);
    if (is_array($data) && isset($data['user']['screen_name'])) {
      print $data['user']['screen_name'] . ': ' . urldecode($data['text']) . "\n";
    }
  }
}

// The OAuth credentials you received when registering your app at Twitter
define("TWITTER_CONSUMER_KEY", "ot0tUgarTYxEBCQrRynDgdMKr");
define("TWITTER_CONSUMER_SECRET", "iUtFcLdY2fDq9jGqIQLfIaXG8ROYHAKv3OMNOtJIVzDZsWztoY");


// The OAuth data for the twitter account
define("OAUTH_TOKEN", "2816508089-1ImNswhZ0uEhq7xBwUAmZpF5hfGDcez4qbVokqN");
define("OAUTH_SECRET", "sf4EVHZ5A3UEv0Tf1Wun4w9jcQq7sHKfUkQUEZSjioXxh");

// Start streaming
$sc = new FilterTrackConsumer(OAUTH_TOKEN, OAUTH_SECRET, Phirehose::METHOD_FILTER);
$sc->setLocations(array(
       //array(-122.75, 36.8, -121.75, 37.8), // San Francisco
       //array(10.1800, 56.1420, 10.2340, 56.1721), // Aarhus
       array(12.5685, 55.6754, 12.5913, 55.6882), // Copenhagen
       //array(-74, 40, -73, 41),             // New York
   ));
$sc->consume();
