<?php
require_once('../lib/Phirehose.php');
require_once('../lib/OauthPhirehose.php');

/**
 * Example of using Phirehose to display a live filtered stream using track words
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
define("TWITTER_CONSUMER_KEY", "TSqgx84SucxJ3yQ8gNCnlNSzY");//5ZpZK45txurjRWA0jAMS6ps96
define("TWITTER_CONSUMER_SECRET", "TuXyHGbW82dM5i1fXTnulgmcS1ln25yR0MCPe9njCpUmGNtYOK"); //4cp43JzQUl155AIpYrUvWsLqHyhlUzXFaABUq7M487kW0hh7MK


// The OAuth data for the twitter account
define("OAUTH_TOKEN", "3172457999-cM13Lq49BI9ZCJJTtGjFQO7EQWIsLONaX4q2EjR"); //747025008-mlocAiUlJWz7U7MPohxhsv8rPScHCgbuAHI6Zs4C
define("OAUTH_SECRET", "3Pf25ggRqUmr2nwu0T0qgPkRO3elsXUbTPkcJ6vKclgFX");//fXQX2uyOvPayEpDtGedvSPHWfgvlqCsHvwVgsYT53PycQ


// Start streaming
$sc = new FilterTrackConsumer(OAUTH_TOKEN, OAUTH_SECRET, Phirehose::METHOD_FILTER);
$sc->setTrack(array('morning', 'goodnight', 'hello', 'the'));
$sc->consume();
