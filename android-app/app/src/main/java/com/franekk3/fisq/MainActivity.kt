package com.franekk3.fisq

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.view.ViewGroup
import android.webkit.WebChromeClient
import android.webkit.WebResourceRequest
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.ComponentActivity
import androidx.activity.compose.BackHandler
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.viewinterop.AndroidView

import com.franekk3.fisq.ui.theme.FisqTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            FisqTheme {
                FisqWebView()
            }
        }
    }
}

@Composable
fun FisqWebView() {
    var backEnabled by remember { mutableStateOf(false) }
    var webView: WebView? by remember { mutableStateOf(null) }

    // This handles the system back button/gesture to go back in WebView history
    BackHandler(enabled = backEnabled) {
        webView?.goBack()
    }

    Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
        AndroidView(
            modifier = Modifier
                .padding(innerPadding)
                .fillMaxSize(),
            factory = { context ->
                WebView(context).apply {
                    layoutParams = ViewGroup.LayoutParams(
                        ViewGroup.LayoutParams.MATCH_PARENT,
                        ViewGroup.LayoutParams.MATCH_PARENT
                    )
                    settings.apply {
                        javaScriptEnabled = true
                        domStorageEnabled = true
                        builtInZoomControls = true
                        displayZoomControls = false
                        // Needed for local file access
                        allowFileAccess = true
                        allowContentAccess = true
                    }
                    webChromeClient = object : WebChromeClient() {
                        override fun onProgressChanged(view: WebView?, newProgress: Int) {
                            super.onProgressChanged(view, newProgress)
                            backEnabled = view?.canGoBack() ?: false
                        }
                    }
                    webViewClient = object : WebViewClient() {
                        override fun shouldOverrideUrlLoading(
                            view: WebView?,
                            request: WebResourceRequest?
                        ): Boolean {
                            val url = request?.url?.toString() ?: return false
                            
                            // Load local assets in the WebView
                            return if (url.startsWith("file:///android_asset/")) {
                                false
                            } else {
                                // Open any external links (http/https) in the browser
                                try {
                                    val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
                                    context.startActivity(intent)
                                    true
                                } catch (e: Exception) {
                                    false
                                }
                            }
                        }

                        override fun doUpdateVisitedHistory(view: WebView?, url: String?, isReload: Boolean) {
                            super.doUpdateVisitedHistory(view, url, isReload)
                            backEnabled = view?.canGoBack() ?: false
                        }

                        override fun onPageFinished(view: WebView?, url: String?) {
                            super.onPageFinished(view, url)
                            backEnabled = view?.canGoBack() ?: false
                        }
                    }
                    // Load the local index.html file
                    loadUrl("file:///android_asset/index.html")
                    webView = this
                }
            },
            update = {
                webView = it
            }
        )
    }
}
