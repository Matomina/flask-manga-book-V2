function forumRequestHeaders() {
  return {
    'Content-Type': 'application/json',
    'X-Requested-With': 'XMLHttpRequest',
  };
}

function escapeHtml(value) {
  return String(value || '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function initials(author) {
  return `${(author.first_name || '').slice(0, 1)}${(author.last_name || '').slice(0, 1)}`;
}

function paragraphs(message) {
  return String(message || '')
    .split('\n')
    .filter((paragraph) => paragraph.trim())
    .map((paragraph) => `<p>${escapeHtml(paragraph)}</p>`)
    .join('');
}

function topicTemplate(topic) {
  return `
    <article class="forum-topic-preview">
      <a class="forum-topic-preview__main" href="${topic.url}">
        <span class="forum-avatar">${escapeHtml(initials(topic.author))}</span>
        <div>
          <h3>${escapeHtml(topic.title)}</h3>
          <p>${escapeHtml(topic.excerpt)}${topic.message.length > 180 ? '...' : ''}</p>
          <small>
            Par ${escapeHtml(topic.author.first_name)} ${escapeHtml(topic.author.last_name)} ·
            ${escapeHtml(topic.created_at)} · ${escapeHtml(topic.author.role)}
          </small>
        </div>
      </a>
      <div class="forum-topic-preview__meta">
        <strong>${topic.reply_count}</strong>
        <span>réponse${topic.reply_count > 1 ? 's' : ''}</span>
      </div>
    </article>
  `;
}

function replyTemplate(reply) {
  return `
    <article class="forum-reply-card">
      <header class="forum-reply-card__header">
        <span class="forum-avatar">${escapeHtml(initials(reply.author))}</span>
        <p class="forum-reply-card__infos">
          <strong>${escapeHtml(reply.author.first_name)} ${escapeHtml(reply.author.last_name)}</strong>
          · ${escapeHtml(reply.created_at)} · ${escapeHtml(reply.author.role)}
        </p>
      </header>
      <div class="forum-reply-card__content">
        ${paragraphs(reply.message)}
      </div>
    </article>
  `;
}

function setForumStatus(message) {
  const status = document.querySelector('[data-forum-status]');

  if (status) {
    status.textContent = message;
  }
}

async function refreshTopics() {
  const list = document.querySelector('[data-forum-topic-list]');

  if (!list) {
    return;
  }

  setForumStatus('Synchronisation');

  const response = await fetch('/forum/api/topics', {
    headers: { 'X-Requested-With': 'XMLHttpRequest' },
  });

  if (!response.ok) {
    setForumStatus('Hors ligne');
    return;
  }

  const data = await response.json();
  list.innerHTML = data.topics.map(topicTemplate).join('');
  setForumStatus('Connecté');
}

async function refreshReplies(topicId) {
  const list = document.querySelector('[data-forum-replies-list]');
  const counter = document.querySelector('[data-forum-reply-count]');

  if (!list || !topicId) {
    return;
  }

  const response = await fetch(`/forum/api/topics/${topicId}`, {
    headers: { 'X-Requested-With': 'XMLHttpRequest' },
  });

  if (!response.ok) {
    return;
  }

  const data = await response.json();

  if (!data.replies.length) {
    list.innerHTML = '<p>Aucune réponse pour le moment. Soyez le premier à participer.</p>';
  } else {
    list.classList.add('forum-replies__list');
    list.innerHTML = data.replies.map(replyTemplate).join('');
  }

  if (counter) {
    counter.textContent = data.reply_count;
  }
}

function initForumRefresh() {
  document.querySelectorAll('[data-forum-refresh]').forEach((button) => {
    button.addEventListener('click', () => {
      const shell = document.querySelector('[data-forum-live]');
      const topicId = shell?.dataset.topicId;

      if (topicId) {
        refreshReplies(topicId);
      } else {
        refreshTopics();
      }
    });
  });
}

function initForumReplyForm() {
  const form = document.querySelector('[data-forum-reply-form]');
  const shell = document.querySelector('[data-topic-id]');

  if (!form || !shell) {
    return;
  }

  form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const textarea = form.querySelector('textarea[name="message"]');
    const message = textarea?.value.trim();

    if (!message) {
      return;
    }

    const response = await fetch(`/forum/${shell.dataset.topicId}/reply`, {
      method: 'POST',
      headers: forumRequestHeaders(),
      body: JSON.stringify({ message }),
    });

    if (!response.ok) {
      return;
    }

    textarea.value = '';
    const data = await response.json();
    const list = document.querySelector('[data-forum-replies-list]');
    const counter = document.querySelector('[data-forum-reply-count]');

    if (list) {
      list.classList.add('forum-replies__list');
      list.innerHTML = data.replies.map(replyTemplate).join('');
    }

    if (counter) {
      counter.textContent = data.reply_count;
    }
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initForumRefresh();
  initForumReplyForm();
});
