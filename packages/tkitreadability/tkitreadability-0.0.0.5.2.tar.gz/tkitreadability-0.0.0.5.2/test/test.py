
#encoding=utf-8
from __future__ import unicode_literals
import sys
# 切换到上级目录
sys.path.append("../")
# 引入本地库
import src
html="""

<article class="markdown-body entry-content container-lg" itemprop="text"><h1><a id="user-content-一个创建库的demo" class="anchor" aria-hidden="true" href="#一个创建库的demo"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M7.775 3.275a.75.75 0 001.06 1.06l1.25-1.25a2 2 0 112.83 2.83l-2.5 2.5a2 2 0 01-2.83 0 .75.75 0 00-1.06 1.06 3.5 3.5 0 004.95 0l2.5-2.5a3.5 3.5 0 00-4.95-4.95l-1.25 1.25zm-4.69 9.64a2 2 0 010-2.83l2.5-2.5a2 2 0 012.83 0 .75.75 0 001.06-1.06 3.5 3.5 0 00-4.95 0l-2.5 2.5a3.5 3.5 0 004.95 4.95l1.25-1.25a.75.75 0 00-1.06-1.06l-1.25 1.25a2 2 0 01-2.83 0z"></path></svg></a>一个创建库的demo</h1>
<p>便于快速创建自己的第三方库</p>
<h2><a id="user-content-快速上传操作" class="anchor" aria-hidden="true" href="#快速上传操作"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" d="M7.775 3.275a.75.75 0 001.06 1.06l1.25-1.25a2 2 0 112.83 2.83l-2.5 2.5a2 2 0 01-2.83 0 .75.75 0 00-1.06 1.06 3.5 3.5 0 004.95 0l2.5-2.5a3.5 3.5 0 00-4.95-4.95l-1.25 1.25zm-4.69 9.64a2 2 0 010-2.83l2.5-2.5a2 2 0 012.83 0 .75.75 0 001.06-1.06 3.5 3.5 0 00-4.95 0l-2.5 2.5a3.5 3.5 0 004.95 4.95l1.25-1.25a.75.75 0 00-1.06-1.06l-1.25 1.25a2 2 0 01-2.83 0z"></path></svg></a>快速上传操作</h2>
<p>可以自动查找依赖，然后上传</p>
<pre><code>sh upload.sh
</code></pre>
<p>文档查看
<a href="https://www.terrychan.org/python_libs_demo/" rel="nofollow">https://www.terrychan.org/python_libs_demo/</a></p>
</article>

"""
Demo =src.tkitＲeadability()
print(Demo.html2text(html))

