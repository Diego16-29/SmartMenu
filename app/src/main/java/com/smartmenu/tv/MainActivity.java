package com.smartmenu.tv;

import android.app.Activity;
import android.os.Bundle;
import android.view.KeyEvent;
import android.view.View;
import android.view.WindowManager;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebResourceRequest;

/** Contenedor Android TV de la interfaz local, sin acceso a red. */
public class MainActivity extends Activity {
    private WebView web;
    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        immersive();
        web = new WebView(this);
        web.setBackgroundColor(0xff151310);
        web.getSettings().setJavaScriptEnabled(true);
        web.getSettings().setDomStorageEnabled(true);
        web.getSettings().setAllowFileAccess(false);
        web.getSettings().setAllowContentAccess(false);
        web.getSettings().setBlockNetworkLoads(true);
        web.setWebViewClient(new WebViewClient() {
            @Override public boolean shouldOverrideUrlLoading(WebView v, WebResourceRequest r) { return true; }
            @Override public boolean shouldOverrideUrlLoading(WebView v, String url) { return true; }
        });
        setContentView(web);
        web.setFocusable(true);
        web.setFocusableInTouchMode(true);
        web.requestFocus();
        web.loadUrl("file:///android_asset/index.html");
    }
    private void immersive() {
        getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_FULLSCREEN | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_LAYOUT_STABLE);
    }
    @Override public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus); if (hasFocus) immersive();
    }
    @Override public boolean dispatchKeyEvent(KeyEvent event) {
        String key;
        switch(event.getKeyCode()) {
            case KeyEvent.KEYCODE_DPAD_UP: key="ArrowUp"; break;
            case KeyEvent.KEYCODE_DPAD_DOWN: key="ArrowDown"; break;
            case KeyEvent.KEYCODE_DPAD_LEFT: key="ArrowLeft"; break;
            case KeyEvent.KEYCODE_DPAD_RIGHT: key="ArrowRight"; break;
            case KeyEvent.KEYCODE_DPAD_CENTER: case KeyEvent.KEYCODE_ENTER: case KeyEvent.KEYCODE_NUMPAD_ENTER: key="Enter"; break;
            case KeyEvent.KEYCODE_BACK: key="Escape"; break;
            default: return super.dispatchKeyEvent(event);
        }
        if (web != null && event.getAction() == KeyEvent.ACTION_DOWN && (event.getRepeatCount()==0 || key.startsWith("Arrow"))) {
            web.evaluateJavascript("window.tvKey && window.tvKey('"+key+"')", result -> {
                if (key.equals("Escape") && "false".equals(result)) finish();
            });
        }
        return true;
    }
    @Override public void onBackPressed() {
        if (web != null) web.evaluateJavascript("window.tvKey && window.tvKey('Escape')", result -> {
            if ("false".equals(result)) finish();
        }); else super.onBackPressed();
    }
    @Override protected void onDestroy() { if(web!=null) { web.destroy(); web=null; } super.onDestroy(); }
}
