<?php
define("TOKEN", "yiquns");
$wechatObj = new wechatCallbackapiTest();
if (isset($_GET['echostr'])) {
    $wechatObj->valid();
}else{
    $wechatObj->responseMsg();
}
class wechatCallbackapiTest
{
    public function valid()
    {
        
        $echoStr = $_GET["echostr"];
        if($this->checkSignature()){
            header('content-type:text');
            ob_clean();
            echo $echoStr;
            exit;
        }
    }
    private function checkSignature()
    {
        $signature = $_GET["signature"];
        $timestamp = $_GET["timestamp"];
        $nonce = $_GET["nonce"];
        $token = TOKEN;
        $tmpArr = array($token, $timestamp, $nonce);
        sort($tmpArr, SORT_STRING);
        $tmpStr = implode( $tmpArr );
        $tmpStr = sha1( $tmpStr );
        if( $tmpStr == $signature ){
            return true;
        }else{
            return false;
        }
    }
    public function responseMsg()
    {
        $postStr = $GLOBALS["HTTP_RAW_POST_DATA"];
        $db = new mysqli("128.199.137.57", "root","","test");
        $db->set_charset("utf8");
        $result = $db->query("SELECT * FROM testTable");  
        $users = array();
        $fR = array();
        while($row = $result->fetch_assoc()){
        $temp = new stdClass();
        $temp->id=$row['dataOne'];
        $users[] = $temp;
         }
        echo json_encode($users);
        $arr = json_decode(json_encode($users,true));
        //print_r($arr);
        //echo $arr[0]->id;
        foreach($arr as $arrs){
        //echo($arrs->id);
        $fR[] = $arrs->id;
        }
        $ffR = implode(", ",$fR);
        if (!empty($postStr)){
            $postObj = simplexml_load_string($postStr, 'SimpleXMLElement', LIBXML_NOCDATA);
            $fromUsername = $postObj->FromUserName;
            $toUsername = $postObj->ToUserName;
            $keyword = trim($postObj->Content);
            $time = time();
            $textTpl = "<xml>
                        <ToUserName><![CDATA[%s]]></ToUserName>
                        <FromUserName><![CDATA[%s]]></FromUserName>
                        <CreateTime>%s</CreateTime>
                        <MsgType><![CDATA[%s]]></MsgType>
                        <Content><![CDATA[%s]]></Content>
                        <FuncFlag>0</FuncFlag>
                        </xml>";
            if($keyword != " " || $keyword == "hi" || $keyword != "")
            {
                $msgType = "text";
                //$contentStr =$ffR;
                $contentStr = "姑娘姑娘你好你好，发送显示排名";
                $resultStr = sprintf($textTpl, $fromUsername, $toUsername, $time, $msgType, $contentStr);
                echo $resultStr;
            }
        }else{
            echo "";
            exit;
        }
    }
}
?>
